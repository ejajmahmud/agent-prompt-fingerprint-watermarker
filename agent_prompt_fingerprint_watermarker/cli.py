"""CLI for agent-prompt-fingerprint-watermarker."""
import sys
import argparse
from .watermark import PromptWatermarker

def main():
    parser = argparse.ArgumentParser(description="Agent Prompt Fingerprint Watermarker CLI")
    parser.add_argument("--demo", action="store_true", help="Run token watermark verification demo")
    args = parser.parse_args()

    if args.demo:
        wm = PromptWatermarker()
        sample = "The quick brown fox jumps over the lazy dog repeatedly in distributed multi-agent systems"
        res = wm.verify_text(sample)
        print(f"[+] Sample verification: watermarked={res.is_watermarked}, z_score={res.z_score}, ratio={res.green_ratio}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
