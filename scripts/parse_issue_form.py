#!/usr/bin/env python3
"""Parse a GitHub issue form submission into metadata JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse


REQUIRED_FIELDS = [
    "team_id",
    "team_name",
    "student_names",
    "model_name",
    "num_parameters",
    "validation_accuracy",
    "validation_f1_macro",
    "predictions_csv_url",
    "ablations_md_url",
]

OPTIONAL_FIELDS = ["notes"]

FIELD_ALIASES = {
    "team_id": ["team_id", "team id", "team identifier"],
    "team_name": ["team_name", "team name"],
    "student_names": ["student_names", "student names", "students"],
    "model_name": ["model_name", "model name"],
    "num_parameters": ["num_parameters", "num parameters", "parameters", "params"],
    "validation_accuracy": ["validation_accuracy", "validation accuracy", "val acc"],
    "validation_f1_macro": [
        "validation_f1_macro",
        "validation f1 macro",
        "val f1",
        "macro f1",
    ],
    "predictions_csv_url": [
        "predictions_csv_url",
        "predictions csv url",
        "predictions url",
    ],
    "ablations_md_url": ["ablations_md_url", "ablations md url", "ablations url"],
    "notes": ["notes", "comments"],
}

NO_RESPONSE_VALUES = {"", "_no response_", "no response", "n/a", "na", "none"}
TEAM_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]{0,63}$")


def normalize_label(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[`*_]+", "", value)
    value = re.sub(r"[\s-]+", "_", value)
    value = re.sub(r"[^a-z0-9_]+", "", value)
    return value.strip("_")


NORMALIZED_ALIASES = {
    normalize_label(alias): field
    for field, aliases in FIELD_ALIASES.items()
    for alias in aliases
}


def clean_value(value: str) -> str:
    value = value.strip()
    if value.strip().lower() in NO_RESPONSE_VALUES:
        return ""
    return value


def parse_issue_body(body: str) -> dict[str, str]:
    headings = list(re.finditer(r"(?m)^#{2,6}\s+(.+?)\s*$", body or ""))
    parsed: dict[str, str] = {}

    for index, match in enumerate(headings):
        label = normalize_label(match.group(1))
        field = NORMALIZED_ALIASES.get(label)
        if not field:
            continue

        start = match.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(body)
        parsed[field] = clean_value(body[start:end])

    return parsed


def parse_int(value: str, field: str) -> int:
    cleaned = re.sub(r"[,_\s]", "", value)
    if not re.fullmatch(r"\d+", cleaned):
        raise ValueError(f"{field} must be an integer.")
    return int(cleaned)


def parse_float(value: str, field: str) -> float:
    cleaned = value.strip().replace(",", ".")
    try:
        return float(cleaned)
    except ValueError as exc:
        raise ValueError(f"{field} must be numeric.") from exc


def require_http_url(value: str, field: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"{field} must be an http(s) direct download URL.")
    return value


def build_metadata(event: dict) -> dict:
    issue = event.get("issue") or {}
    body = issue.get("body") or ""
    values = parse_issue_body(body)

    missing = [field for field in REQUIRED_FIELDS if not values.get(field)]
    if missing:
        raise ValueError(f"Missing required issue form fields: {', '.join(missing)}.")

    team_id = values["team_id"].strip()
    if not TEAM_ID_RE.fullmatch(team_id):
        raise ValueError(
            "team_id may contain only letters, numbers, underscores, periods, "
            "and hyphens, and must be 1-64 characters."
        )

    num_parameters = parse_int(values["num_parameters"], "num_parameters")
    validation_accuracy = parse_float(values["validation_accuracy"], "validation_accuracy")
    validation_f1_macro = parse_float(values["validation_f1_macro"], "validation_f1_macro")

    metadata = {
        "team_id": team_id,
        "team_name": values["team_name"].strip(),
        "student_names": values["student_names"].strip(),
        "model_name": values["model_name"].strip(),
        "num_parameters": num_parameters,
        "validation_accuracy": validation_accuracy,
        "validation_f1_macro": validation_f1_macro,
        "issue_number": int(issue.get("number") or 0),
        "submitted_at": datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z"),
        "predictions_csv_url": require_http_url(
            values["predictions_csv_url"].strip(), "predictions_csv_url"
        ),
        "ablations_md_url": require_http_url(
            values["ablations_md_url"].strip(), "ablations_md_url"
        ),
        "notes": values.get("notes", "").strip(),
    }

    if metadata["issue_number"] <= 0:
        raise ValueError("Could not determine the GitHub issue number from the event.")

    return metadata


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--event-path", required=True, help="Path to GITHUB_EVENT_PATH JSON.")
    parser.add_argument("--output", required=True, help="Where to write metadata JSON.")
    args = parser.parse_args()

    try:
        event = json.loads(Path(args.event_path).read_text(encoding="utf-8"))
        metadata = build_metadata(event)
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"Submission form parsing failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

