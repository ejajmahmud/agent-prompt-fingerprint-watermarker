"""Statistical green-list token watermarking for agent outputs."""
import hashlib
import math
from typing import Dict, List, Optional, Tuple, Any

class WatermarkResult:
    def __init__(self, is_watermarked: bool, z_score: float, green_ratio: float, total_tokens: int):
        self.is_watermarked = is_watermarked
        self.z_score = z_score
        self.green_ratio = green_ratio
        self.total_tokens = total_tokens

class PromptWatermarker:
    """Embeds and verifies statistical green-list token distribution watermarks."""

    def __init__(self, key: str = "antigravity_master_secret_2026", gamma: float = 0.5, z_threshold: float = 3.0):
        self.key = key
        self.gamma = gamma  # Target proportion of green tokens
        self.z_threshold = z_threshold

    def is_green_token(self, prev_token: str, current_token: str) -> bool:
        h = hashlib.sha256(f"{self.key}:{prev_token}:{current_token}".encode("utf-8")).hexdigest()
        val = int(h[:8], 16) / 0xFFFFFFFF
        return val < self.gamma

    def verify_text(self, text: str) -> WatermarkResult:
        tokens = text.split()
        if len(tokens) < 5:
            return WatermarkResult(False, 0.0, 0.0, len(tokens))

        green_count = 0
        total_pairs = len(tokens) - 1

        for i in range(total_pairs):
            if self.is_green_token(tokens[i], tokens[i + 1]):
                green_count += 1

        green_ratio = green_count / total_pairs
        expected = total_pairs * self.gamma
        variance = total_pairs * self.gamma * (1.0 - self.gamma)
        std_dev = math.sqrt(variance)

        z_score = (green_count - expected) / max(std_dev, 1e-6)
        is_watermarked = z_score >= self.z_threshold

        return WatermarkResult(is_watermarked, round(z_score, 3), round(green_ratio, 3), len(tokens))
