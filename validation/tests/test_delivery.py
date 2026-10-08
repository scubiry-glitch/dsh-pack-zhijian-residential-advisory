import copy
import hashlib
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from validate_delivery import validate_delivery

ROLES = ['price_full', 'price_external', 'rent_full', 'rent_external']
class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.context = dict(case_id='case1', attempt_id='try1', job_id='job1', city_code='350100', input_sha256='a'*64, release_id='demo-v2')
        self.manifest = dict(self.context, status='succeeded', quality_status='passed', files=[])
        for role in ROLES:
            content = (role + ' test fixture, not a real report').encode()
            (self.root / (role+'.docx')).write_bytes(content)
            self.manifest['files'].append(dict(role=role, file_id=role, filename=role+'.docx', sha256=hashlib.sha256(content).hexdigest(), size_bytes=len(content)))
    def test_complete_without_approval_or_roles(self):
        self.assertEqual(validate_delivery(self.manifest, self.context, self.root), [])
    def test_partial_and_duplicate(self):
        for files in [self.manifest['files'][:2], [self.manifest['files'][0]]*4]:
            m = dict(self.manifest, files=files)
            self.assertTrue(validate_delivery(m, self.context, self.root))
    def test_binding_mismatch(self):
        for field in self.context:
            m = dict(self.manifest, **{field:'wrong'})
            self.assertTrue(validate_delivery(m, self.context, self.root), field)
    def test_changed_bytes(self):
        (self.root/'price_full.docx').write_bytes(b'tampered')
        self.assertTrue(validate_delivery(self.manifest, self.context, self.root))
    def test_failed_job_and_quality(self):
        for k, v in [('status','failed'),('quality_status','pending')]:
            self.assertTrue(validate_delivery(dict(self.manifest, **{k:v}), self.context, self.root))
    def test_path_escape(self):
        self.manifest['files'][0]['filename'] = '../outside.docx'
        self.assertTrue(validate_delivery(self.manifest, self.context, self.root))
    def test_duplicate_file_ids(self):
        self.manifest['files'][1]['file_id'] = self.manifest['files'][0]['file_id']
        self.assertTrue(validate_delivery(self.manifest, self.context, self.root))
    def test_missing_expected_binding(self):
        self.assertTrue(validate_delivery(self.manifest, {}, self.root))
if __name__ == '__main__': unittest.main()
