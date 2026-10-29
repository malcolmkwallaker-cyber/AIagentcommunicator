import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
from malcolm_os import approvals, slack, tiers  # noqa: E402

A = "U123"
OK = [{"name": "white_check_mark", "users": [A]}]


class Tests(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(tiers.classify("research"), tiers.TIER_1)
        self.assertEqual(tiers.classify("change_code"), tiers.TIER_2)
        self.assertEqual(tiers.classify("send_email"), tiers.TIER_3)
        self.assertEqual(tiers.classify("create_repo"), tiers.TIER_3)
        self.assertEqual(tiers.classify("unknown_thing"), tiers.TIER_3)

    def test_decide(self):
        self.assertEqual(approvals.decide(OK, A, "1000", now=1001), "approved")
        self.assertEqual(approvals.decide([{"name": "x", "users": [A]}], A, "1000", now=1001), "rejected")
        self.assertEqual(approvals.decide([{"name": "white_check_mark", "users": ["U999"]}], A, "1000", now=1001), "pending")
        self.assertEqual(approvals.decide([], A, "1000", now=1000 + 72 * 3600 + 1), "expired")
        self.assertEqual(approvals.decide([{"name": "white_check_mark::skin-tone-2", "users": [A]}], A, "1000", now=1001), "approved")

    def test_authorize_needs_id(self):
        self.assertFalse(approvals.authorize("send_email", None, A)[0])
        self.assertTrue(approvals.authorize("research", None, A)[0])

    def test_channels(self):
        self.assertEqual(slack.normalize_channel("#agent-cirql"), "agent-cirql")
        with self.assertRaises(ValueError):
            slack.normalize_channel("general")

    def test_handoff(self):
        t = slack.format_handoff("a", "b", "t", "c", "d")
        self.assertTrue(t.startswith("FROM: a\nTO: b\nTASK: t"))
        with self.assertRaises(ValueError):
            slack.format_handoff("a", "", "t", "c", "d")


if __name__ == "__main__":
    unittest.main()
