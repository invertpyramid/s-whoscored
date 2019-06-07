"""
Tests for WhoScored Spiders and related middlewares, modules and functions
"""
from pathlib import Path

SAMPLES: Path = Path(__file__).parent / "samples"

RESPONSE_FAILED = SAMPLES / "response_failed.html"
RESPONSE_SUCCEED = SAMPLES / "response_succeed.html"
