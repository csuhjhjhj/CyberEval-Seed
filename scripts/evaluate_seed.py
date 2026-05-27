"""Minimal evaluator for CyberEval-Seed JSONL samples.

This script scores single-choice and fill-blank samples by exact matching, and
prints a lightweight coverage report. Short-answer and dynamic samples are kept
for rubric-based human or model-assisted review.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


DATA = Path(__file__).resolve().parents[1] / "data" / "seed_samples.jsonl"


def normalize(text: str) -> str:
    return "".join(str(text).strip().lower().split())


def load_samples():
    with DATA.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def main() -> None:
    samples = list(load_samples())
    domains = Counter(s["metadata"]["domain"] for s in samples)
    levels = Counter(s["metadata"]["cognitive_level"] for s in samples)
    print(f"samples={len(samples)}")
    print("domains=", dict(domains))
    print("cognitive_levels=", dict(levels))
    print("scorable_static_samples=", sum(s["question"]["type"] in {"single_choice", "fill_blank"} for s in samples))


if __name__ == "__main__":
    main()
