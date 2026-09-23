import unittest
from recruitment import parse_resume,extract_evidence,evaluate,decide
R={'id':'x','name':'Sample','skills':['Python'],'years':1,'evidence':['Built Python API']};J={'id':'j','skills':['Python','QA']}
class TestRecruitment(unittest.TestCase):
    def test_parse(self):self.assertEqual(parse_resume(R)['id'],'x')
    def test_invalid(self):self.assertRaises(ValueError,parse_resume,{})
    def test_trace(self):self.assertEqual(extract_evidence(R,J)[0]['source'],'Built Python API')
    def test_no_unsupported_credit(self):self.assertEqual(evaluate(R,J)['score'],50)
    def test_human_gate(self):self.assertEqual(evaluate(R,J)['state'],'HUMAN_REVIEW')
    def test_no_auto_decision(self):self.assertIsNone(evaluate(R,J)['decision'])
    def test_empty_reviewer(self):self.assertRaises(ValueError,decide,evaluate(R,J),'','DECLINE','x')
    def test_reason_required(self):self.assertRaises(ValueError,decide,evaluate(R,J),'Human','HOLD','')
    def test_audited_decision(self):self.assertEqual(decide(evaluate(R,J),'Human','INTERVIEW','Review evidence')['state'],'HUMAN_DECIDED')
    def test_no_evidence_risk(self):self.assertIn('NO_EVIDENCE',evaluate({'id':'x','name':'x','skills':[],'years':0,'evidence':[]},J)['risk'])
    def test_unsupported_claim_risk(self):self.assertIn('SELF_REPORTED_UNSUPPORTED',evaluate({'id':'x','name':'x','skills':['QA'],'years':0,'evidence':[]},J)['risk'])
    def test_conflict_flag(self):self.assertIn('CONFLICT_FLAG',evaluate({**R,'conflicts':['fictional inconsistency']},J)['risk'])
    def test_invalid_action(self):self.assertRaises(ValueError,decide,evaluate(R,J),'Human','HIRE','reason')
if __name__=='__main__':unittest.main()
