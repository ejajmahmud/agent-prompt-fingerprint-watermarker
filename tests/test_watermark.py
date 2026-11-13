"""Unit tests for agent-prompt-fingerprint-watermarker."""
import unittest
from agent_prompt_fingerprint_watermarker.watermark import PromptWatermarker

class TestPromptWatermarker(unittest.TestCase):
    def setUp(self):
        self.wm = PromptWatermarker(gamma=0.5, z_threshold=2.5)

    def test_short_text(self):
        res = self.wm.verify_text("short prompt")
        self.assertFalse(res.is_watermarked)

    def test_green_token_consistency(self):
        b1 = self.wm.is_green_token("hello", "world")
        b2 = self.wm.is_green_token("hello", "world")
        self.assertEqual(b1, b2)

    def test_statistical_verification_structure(self):
        res = self.wm.verify_text("one two three four five six seven eight nine ten")
        self.assertIsInstance(res.z_score, float)
        self.assertGreaterEqual(res.green_ratio, 0.0)
        self.assertLessEqual(res.green_ratio, 1.0)

if __name__ == "__main__":
    unittest.main()
