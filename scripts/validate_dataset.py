from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "seed_samples.jsonl"

REQUIRED_TOP_LEVEL = {"id", "question", "answer", "metadata", "evaluation"}
REQUIRED_METADATA = {"domain", "knowledge_point", "difficulty", "cognitive_level", "sensitivity", "source"}
VALID_TYPES = {"single_choice", "fill_blank", "short_answer", "dynamic"}


def load_samples() -> list[dict]:
    samples = []
    with DATA.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            if not line.strip():
                continue
            try:
                sample = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"Line {line_no}: invalid JSON: {exc}") from exc
            samples.append(sample)
    return samples


def validate_sample(sample: dict) -> list[str]:
    errors: list[str] = []
    sid = sample.get("id", "<missing-id>")
    missing = REQUIRED_TOP_LEVEL - set(sample)
    if missing:
        errors.append(f"{sid}: missing top-level fields {sorted(missing)}")

    question = sample.get("question", {})
    qtype = question.get("type")
    if qtype not in VALID_TYPES:
        errors.append(f"{sid}: invalid question.type {qtype!r}")
    if not question.get("stem"):
        errors.append(f"{sid}: missing question.stem")

    answer = sample.get("answer", {})
    if not answer.get("gold") or not answer.get("rubric"):
        errors.append(f"{sid}: answer.gold and answer.rubric are required")

    metadata = sample.get("metadata", {})
    missing_metadata = REQUIRED_METADATA - set(metadata)
    if missing_metadata:
        errors.append(f"{sid}: missing metadata fields {sorted(missing_metadata)}")

    return errors


def main() -> None:
    samples = load_samples()
    errors: list[str] = []
    for sample in samples:
        errors.extend(validate_sample(sample))
    if errors:
        print("validation_failed")
        for error in errors:
            print(error)
        raise SystemExit(1)
    print(f"validation_ok samples={len(samples)}")


if __name__ == "__main__":
    main()
