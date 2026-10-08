"""Validate original-file delivery integrity, not DOCX contents or valuation quality."""
import argparse
import hashlib
import json
import re
from pathlib import Path

ROLES = {'price_full', 'price_external', 'rent_full', 'rent_external'}
BINDINGS = ('case_id', 'attempt_id', 'job_id', 'city_code', 'input_sha256', 'release_id')

def validate_delivery(manifest, expected, directory):
    errors = []
    if not isinstance(manifest, dict) or not isinstance(expected, dict):
        return ['manifest and expected must be objects']
    for field in BINDINGS:
        if not isinstance(expected.get(field), str) or not expected[field] or manifest.get(field) != expected[field]:
            errors.append('binding mismatch: ' + field)
    if manifest.get('status') != 'succeeded' or manifest.get('quality_status') != 'passed':
        errors.append('job or quality not successful')
    files = manifest.get('files')
    if not isinstance(files, list) or len(files) != 4 or not all(isinstance(f, dict) for f in files):
        return errors + ['exactly four file records required']
    if sorted(str(f.get('role')) for f in files) != sorted(ROLES):
        errors.append('four unique report roles required')
    root = Path(directory).resolve()
    ids, names = set(), set()
    for f in files:
        file_id, name = f.get('file_id'), f.get('filename')
        if not isinstance(file_id, str) or not file_id or file_id in ids:
            errors.append('invalid or duplicate file_id')
        else:
            ids.add(file_id)
        if not isinstance(name, str) or any(ord(c) < 32 for c in name) or '/' in name or '\\' in name or not name.endswith('.docx') or name in names:
            errors.append('invalid or duplicate filename')
            continue
        names.add(name)
        path = root / name
        if path.is_symlink() or path.resolve().parent != root or not path.is_file():
            errors.append('missing or unsafe file: ' + name)
            continue
        size = f.get('size_bytes')
        if type(size) is not int or size <= 0 or path.stat().st_size != size:
            errors.append('size mismatch: ' + name)
        digest = f.get('sha256')
        if not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest):
            errors.append('invalid hash: ' + name)
        else:
            with path.open('rb') as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            if actual != digest:
                errors.append('hash mismatch: ' + name)
    return errors

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manifest', type=Path)
    parser.add_argument('expected', type=Path, help='Trusted current task binding, not copied from response')
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    errors = validate_delivery(json.loads(args.manifest.read_text()), json.loads(args.expected.read_text()), args.directory)
    print(json.dumps({'ok': not errors, 'errors': errors}, ensure_ascii=False, indent=2))
    raise SystemExit(bool(errors))
