import sys
import os
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from backend.main import app

class TestIPLAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_health(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "ok")

    def test_metadata(self):
        res = self.client.get("/api/metadata")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("teams", data)
        self.assertIn("venues", data)
        self.assertGreater(len(data["teams"]), 0)

    def test_predict(self):
        payload = {
            "batting_team": "Chennai Super Kings",
            "bowling_team": "Mumbai Indians",
            "venue": "Wankhede Stadium, Mumbai",
            "current_score": 140,
            "wickets_fallen": 2,
            "overs_completed": 15.0,
            "target_runs": 175,
            "toss_winner": "Chennai Super Kings",
            "toss_decision": "field"
        }
        res = self.client.post("/api/predict", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("chasing_team_win_prob", data)
        self.assertIn("defending_team_win_prob", data)
        self.assertAlmostEqual(data["chasing_team_win_prob"] + data["defending_team_win_prob"], 100.0, places=1)
        print("Test Predict Response:", data)

    def test_simulate(self):
        res = self.client.get("/api/simulate-match/match_2023_final")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("ball_by_ball", data)
        self.assertGreater(len(data["ball_by_ball"]), 0)

if __name__ == '__main__':
    unittest.main()
