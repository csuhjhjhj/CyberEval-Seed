from __future__ import annotations

import csv
import json
from pathlib import Path

from flask import Flask, jsonify, send_from_directory


BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
STATIC = BASE / "static"

app = Flask(__name__, static_folder=str(STATIC), static_url_path="")


def read_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_jsonl(path: Path):
    rows = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def read_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


@app.get("/")
def index():
    return send_from_directory(STATIC, "index.html")


@app.get("/api/summary")
def summary():
    project = read_json(DATA / "project_summary.json")
    samples = read_jsonl(DATA / "seed_samples.jsonl")
    coverage = read_csv(DATA / "coverage_matrix.csv")

    domains = {}
    types = {}
    levels = {}
    for item in samples:
        domains[item["metadata"]["domain"]] = domains.get(item["metadata"]["domain"], 0) + 1
        types[item["question"]["type"]] = types.get(item["question"]["type"], 0) + 1
        levels[item["metadata"]["cognitive_level"]] = levels.get(item["metadata"]["cognitive_level"], 0) + 1

    return jsonify(
        {
            "project": project,
            "survey": {
                "github": "https://github.com/csuhjhjhj/cybersecurity-llm-benchmark-survey",
                "title": "网络安全大模型评测基准与测评集构建技术调研",
                "findings": [
                    "通用大模型评测框架已经较成熟，但网络安全场景需要更细的专业知识划分、可追溯来源依据和面向防御任务的评分规则。",
                    "现有安全类数据集多集中在问答、CTF 或少量漏洞知识，覆盖范围、题型结构、动态交互和中文场景仍有扩展空间。",
                    "网络安全测评集需要同时处理专业性和可公开性，适合采用公开知识、脱敏场景和防御导向任务的构建方式。",
                ],
            },
            "seed": {
                "sample_count": len(samples),
                "domains": domains,
                "question_types": types,
                "cognitive_levels": levels,
                "coverage": coverage,
                "github": "https://github.com/csuhjhjhj/CyberEval-Seed",
            },
        }
    )


@app.get("/api/samples")
def samples():
    return jsonify(read_jsonl(DATA / "seed_samples.jsonl"))


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "cybereval-showcase"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8060)
