import unittest
from app.agent import VagabondAgent

class TestVagabondAgent(unittest.TestCase):
    def setUp(self):
        self.agent = VagabondAgent(system_instruction="You are Vagabond.")

    def test_driving_guardrail_success(self):
        result = self.agent.process_driving_log(3.5)
        self.assertEqual(result["status"], "SUCCESS")

    def test_driving_guardrail_hitl_trigger(self):
        result = self.agent.process_driving_log(5.0)
        self.assertEqual(result["status"], "PAUSED_HITL")

if __name__ == '__main__':
    unittest.main()
