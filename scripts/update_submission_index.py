#!/usr/bin/env python3
"""Archive submissions and regenerate leaderboard indexes."""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
import uuid
from pathlib import Path


LOG_COLUMNS = [
    "submission_id",
    "submitted_at",
    "issue_number",
    "team_id",
    "team_name",
    "student_names",
    "model_name",
    "num_parameters",
    "validation_accuracy",
    "validation_f1_macro",
    "predictions_csv_url",
    "ablations_md_url",
    "status",
    "message",
]


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def ensure_log(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists() or log_path.stat().st_size == 0:
        with log_path.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=LOG_COLUMNS)
            writer.writeheader()


def append_log_row(log_path: Path, metadata: dict, status: str, message: str) -> None:
    ensure_log(log_path)
    row = {
        "submission_id": uuid.uuid4().hex,
        "submitted_at": metadata["submitted_at"],
        "issue_number": metadata["issue_number"],
        "team_id": metadata["team_id"],
        "team_name": metadata["team_name"],
        "student_names": metadata["student_names"],
        "model_name": metadata["model_name"],
        "num_parameters": metadata["num_parameters"],
        "validation_accuracy": metadata["validation_accuracy"],
        "validation_f1_macro": metadata["validation_f1_macro"],
        "predictions_csv_url": metadata["predictions_csv_url"],
        "ablations_md_url": metadata["ablations_md_url"],
        "status": status,
        "message": " ".join(message.split()),
    }

    with log_path.open("a", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=LOG_COLUMNS)
        writer.writerow(row)


def archive_latest(repo_root: Path, work_dir: Path, metadata: dict) -> None:
    latest_dir = repo_root / "submissions" / metadata["team_id"] / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)

    predictions = work_dir / "predictions.csv"
    ablations = work_dir / "ABLATIONS.md"
    if not predictions.exists():
        raise ValueError(f"Missing staged file: {predictions}")
    if not ablations.exists():
        raise ValueError(f"Missing staged file: {ablations}")

    shutil.copyfile(predictions, latest_dir / "predictions.csv")
    shutil.copyfile(ablations, latest_dir / "ABLATIONS.md")
    (latest_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def read_log_rows(log_path: Path) -> list[dict[str, str]]:
    ensure_log(log_path)
    with log_path.open(newline="", encoding="utf-8") as input_file:
        return list(csv.DictReader(input_file))


def escape_markdown_cell(value: object) -> str:
    text = "" if value is None else str(value)
    text = " ".join(text.split())
    return text.replace("|", r"\|")


def regenerate_latest_markdown(log_path: Path, output_path: Path) -> None:
    rows = read_log_rows(log_path)
    latest_by_team: dict[str, dict[str, str]] = {}

    for row in rows:
        if row.get("status") == "accepted":
            latest_by_team[row["team_id"]] = row

    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Latest Submissions",
        "",
        "| Team ID | Team name | Model | Params | Val Acc | Val F1 | Last submission | Issue |",
        "| --- | --- | --- | ---: | ---: | ---: | --- | --- |",
    ]

    for team_id in sorted(latest_by_team):
        row = latest_by_team[team_id]
        issue_number = row.get("issue_number", "")
        issue_cell = f"#{issue_number}" if issue_number else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_markdown_cell(row.get("team_id")),
                    escape_markdown_cell(row.get("team_name")),
                    escape_markdown_cell(row.get("model_name")),
                    escape_markdown_cell(row.get("num_parameters")),
                    escape_markdown_cell(row.get("validation_accuracy")),
                    escape_markdown_cell(row.get("validation_f1_macro")),
                    escape_markdown_cell(row.get("submitted_at")),
                    escape_markdown_cell(issue_cell),
                ]
            )
            + " |"
        )

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, help="Path to metadata JSON.")
    parser.add_argument(
        "--work-dir",
        default=".submission_work",
        help="Directory containing staged submission files.",
    )
    parser.add_argument(
        "--status",
        required=True,
        choices=["accepted", "rejected"],
        help="Submission status to record.",
    )
    parser.add_argument("--message", required=True, help="Status message to record.")
    parser.add_argument("--repo-root", default=None, help="Repository root override.")
    args = parser.parse_args()

    try:
        repo_root = Path(args.repo_root).resolve() if args.repo_root else repo_root_from_script()
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        log_path = repo_root / "leaderboard" / "submissions_log.csv"
        latest_markdown_path = repo_root / "leaderboard" / "latest_submissions.md"

        if args.status == "accepted":
            archive_latest(repo_root, Path(args.work_dir), metadata)

        append_log_row(log_path, metadata, args.status, args.message)
        regenerate_latest_markdown(log_path, latest_markdown_path)
    except Exception as exc:
        print(f"Could not update submission index: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

