import unittest
import asyncio
from app.agent import VagabondAgent

# 1. Golden Evaluation Dataset mapping expected routes to distances
GOLDEN_DATASET = {
    ("Munich", "Innsbruck"): {"expected_km": 151, "expected_duration": 2.0},
    ("Innsbruck", "Cortina"): {"expected_km": 160, "expected_duration": 2.5}
}

class RegressionTestSuite(unittest.TestCase):
    def test_regression_against_golden_dataset(self):
        """Validates current travel estimations against our Golden baseline."""
        from app.tools import calculate_route_distance
        import json
        
        for (origin, dest), golden in GOLDEN_DATASET.items():
            result_str = calculate_route_distance(origin, dest)
            result = json.loads(result_str)
            
            # Assertions against the Golden Dataset
            self.assertEqual(result["distance_km"], golden["expected_km"])
            self.assertEqual(result["duration_hours"], golden["expected_duration"])

    def test_async_database_workflow(self):
        """Tests asynchronous database and multi-agent pipeline."""
        agent = VagabondAgent(session_id="test_session_99")
        
        # Run async workflow
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        res = loop.run_until_complete(agent.ingest_message_async("Plan route to kosurik@google.com"))
        
        # Asserts state saved successfully and PII was scrubbed in history
        self.assertTrue(res["state_persisted"])
        self.assertEqual(agent.history[-1]["content"], "Plan route to [REDACTED_EMAIL]")

if __name__ == '__main__':
    unittest.main()
