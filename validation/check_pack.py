"""Validate local pack references and content-tree hashes; not the platform schema/runtime."""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = 'generated/build-manifest.json'

def payloads(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and not set(p.relative_to(root).parts) & {'.git', '__pycache__'} and p.name != '.DS_Store' and p.suffix != '.pyc' and p.relative_to(root).as_posix() != MANIFEST)

def inventory(root):
    return [{'path':p.relative_to(root).as_posix(), 'sha256':hashlib.sha256(p.read_bytes()).hexdigest(), 'size':p.stat().st_size} for p in payloads(root)]

def check(root, hashes=True):
    errors=[]
    def require(ok, message):
        if not ok: errors.append(message)
    def read(path):return json.loads((root/path).read_text())
    pack=read('pack.json'); version=pack['version']
    for p in payloads(root):
        require(p.suffix not in {'.zip','.docx','.csv.gz','.pkl','.joblib','.parquet','.sqlite','.db'}, 'private payload: '+str(p))
        if p.suffix=='.json':
            obj=json.loads(p.read_text())
            if isinstance(obj,dict) and 'version' in obj: require(obj['version']==version,'component version: '+str(p))
    with (root/'data-contracts/capability-contract.csv').open(newline='') as f: caps=[r['capability'] for r in csv.DictReader(f)]
    require(len(caps)==len(set(caps)), 'duplicate capability')
    catalog=read('data-contracts/skill-catalog.json')
    skills={s['id'] for s in catalog['skills']}
    for s in catalog['skills']:require((root/s['distributionPath']).is_file(), 'missing skill '+s['id'])
    scenarios={p.stem:json.loads(p.read_text()) for p in (root/'scenarios').glob('*.json')}
    routes=read('routing/intents.json')['routes']
    for route in routes:
        require(route['scenario'] in scenarios,'unknown route '+route['scenario'])
    require(routes[0]['scenario']=='single-home-four-reports','four-report route must be first')
    for sid,s in scenarios.items():
        t=read('team-templates/'+s['teamTemplate']+'.json')
        o=read('output-templates/'+s['outputTemplate']+'.json')
        q=read('quality-policies/'+s['qualityPolicy']+'.json')
        require(t['scenarioId']==sid and o['appliesToScenario']==sid, 'scenario reference '+sid)
        require(s['skill']['id'] in skills,'missing scenario skill '+sid)
        require(len(s['tasks'])==len(t['tasks']), 'task length mismatch '+sid)
        seen=set(); slots={slot['id'] for slot in t['slots']}
        for i,task in enumerate(t['tasks']):
            require(task['id'] not in seen and set(task['dependsOn']) <= seen, 'invalid DAG '+sid)
            require(task['role'] in slots,'unbound role '+sid)
            require(task['description']==s['tasks'][i]['description'], 'scenario/team description drift '+sid)
            require(task['dependsOn']==['t'+str(j) for j in s['tasks'][i]['dependsOn']], 'DAG drift '+sid)
            require(set(task['allowedCapabilities']) <= set(caps), 'unknown task capability '+sid)
            affinities=read('experts/'+task['role']+'.json')['toolAffinities']
            require(set(task['allowedCapabilities']) <= set(affinities),'expert capability drift '+sid)
            seen.add(task['id'])
        gate_ids={g['id'] for g in q['gates']}
        for gate in t['gates']:require(gate['policy']==q['id'] and gate['gate'] in gate_ids,'unknown gate '+sid)
        for d in t['deliverables']:require(set(d['fromTasks'])<=seen and d['outputTemplate']==o['id'],'invalid deliverable '+sid)
    policy=read('data-contracts/v2-capabilities.json')
    require(len(policy['capabilities'])==6,'six v2 capabilities required')
    require(set(c['capability'] for c in policy['capabilities'])<=set(caps),'v2 CSV drift')
    require(policy['deliveryPolicy']['reportRoleGating'] is False and policy['deliveryPolicy']['manualApprovalRequired'] is False,'unexpected delivery approval gate')
    require(set(policy['deliveryPolicy']['roles'])=={'price_full','price_external','rent_full','rent_external'},'incorrect report roles')
    for c in policy['capabilities']:
        if c['capability'].endswith('report.generate'):require(c['readOnly'] is False,'generation cannot be readOnly')
    for p in payloads(root):
        if p.suffix in {'.md','.json'} and p.relative_to(root).parts[0] not in {'docs','validation','generated'}:
            text=p.read_text()
            for banned in ['只能由授权人工流程写入','对外交付必须由授权人工批准','不替代授权人工外发审批']:
                require(banned not in text, 'stale approval rule '+str(p))
    if hashes:
        m=read(MANIFEST); actual=inventory(root)
        require(m['source_files']==actual,'content manifest mismatch')
        require(m['source_file_count']==len(actual) and m['pack_version']==version,'manifest metadata mismatch')
    return errors

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--build',action='store_true');args=parser.parse_args()
    errors=check(ROOT,hashes=not args.build)
    if args.build and not errors:
        report={'pack_id':'zhijian-residential-advisory','version':'0.3.0','scope':'local_references_and_contracts_only','status':'passed','errors':[], 'not_performed':['platform_schema_import','provider_registration','target_container_runtime','real_four_docx_download_and_visual_acceptance']}
        (ROOT/'validation/validation-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
        files=inventory(ROOT)
        (ROOT/MANIFEST).write_text(json.dumps({'pack_id':'zhijian-residential-advisory','pack_version':'0.3.0','schema_version':'zhijian_pack_build_manifest.v1','source_file_count':len(files),'source_files':files},ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'ok':not errors,'errors':errors,'scope':'local_pack_only'},ensure_ascii=False,indent=2))
    raise SystemExit(bool(errors))
