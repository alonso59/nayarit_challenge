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
    "student_id",
    "student_name",
    "model_name",
    "num_parameters",
    "validation_accuracy",
    "validation_f1_macro",
    "submission_zip_url",
    "test_accuracy",
    "test_macro_f1",
    "efficiency_score",
    "final_score",
    "status",
    "message",
]


def repo_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def participant_id(metadata: dict) -> str:
    return metadata.get("student_id") or metadata.get("team_id") or ""


def participant_name(metadata: dict) -> str:
    return (
        metadata.get("student_name")
        or metadata.get("student_names")
        or metadata.get("team_name")
        or ""
    )


def ensure_log(log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists() or log_path.stat().st_size == 0:
        with log_path.open("w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=LOG_COLUMNS)
            writer.writeheader()


def append_log_row(
    log_path: Path,
    metadata: dict,
    status: str,
    message: str,
    metrics: dict | None = None,
) -> None:
    ensure_log(log_path)
    metrics = metrics or {}
    row = {
        "submission_id": uuid.uuid4().hex,
        "submitted_at": metadata["submitted_at"],
        "issue_number": metadata["issue_number"],
        "student_id": participant_id(metadata),
        "student_name": participant_name(metadata),
        "model_name": metadata["model_name"],
        "num_parameters": metadata["num_parameters"],
        "validation_accuracy": metadata["validation_accuracy"],
        "validation_f1_macro": metadata["validation_f1_macro"],
        "submission_zip_url": metadata.get("submission_zip_url", ""),
        "test_accuracy": metrics.get("accuracy", ""),
        "test_macro_f1": metrics.get("macro_f1", ""),
        "efficiency_score": metrics.get("efficiency_score", ""),
        "final_score": metrics.get("final_score", ""),
        "status": status,
        "message": " ".join(message.split()),
    }

    with log_path.open("a", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=LOG_COLUMNS)
        writer.writerow(row)


def archive_latest(repo_root: Path, work_dir: Path, metadata: dict, metrics: dict | None) -> None:
    latest_dir = repo_root / "submissions" / participant_id(metadata) / "latest"
    latest_dir.mkdir(parents=True, exist_ok=True)

    predictions = work_dir / "predictions.csv"
    ablations = work_dir / "ABLATIONS.md"
    metrics_path = work_dir / "metrics.json"
    if not predictions.exists():
        raise ValueError(f"Missing staged file: {predictions}")
    if not ablations.exists():
        raise ValueError(f"Missing staged file: {ablations}")
    if metrics is not None and not metrics_path.exists():
        raise ValueError(f"Missing staged file: {metrics_path}")

    shutil.copyfile(predictions, latest_dir / "predictions.csv")
    shutil.copyfile(ablations, latest_dir / "ABLATIONS.md")
    if metrics is not None:
        shutil.copyfile(metrics_path, latest_dir / "metrics.json")
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


def row_student_id(row: dict[str, str]) -> str:
    return row.get("student_id") or row.get("team_id") or ""


def row_student_name(row: dict[str, str]) -> str:
    return row.get("student_name") or row.get("student_names") or row.get("team_name") or ""


def regenerate_latest_markdown(log_path: Path, output_path: Path) -> None:
    rows = read_log_rows(log_path)
    latest_by_student: dict[str, dict[str, str]] = {}

    for row in rows:
        student_id = row_student_id(row)
        if row.get("status") == "accepted" and student_id:
            latest_by_student[student_id] = row

    ranked_rows = sorted(
        latest_by_student.values(),
        key=lambda row: (
            float(row.get("final_score") or 0),
            float(row.get("test_macro_f1") or 0),
            float(row.get("test_accuracy") or 0),
        ),
        reverse=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Latest Submissions",
        "",
        (
            "| Rank | Student ID | Student name | Model | Params | Test Acc | Test F1 | "
            "Efficiency | Final score | Last submission | Issue |"
        ),
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]

    for rank, row in enumerate(ranked_rows, start=1):
        issue_number = row.get("issue_number", "")
        issue_cell = f"#{issue_number}" if issue_number else ""
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_markdown_cell(rank),
                    escape_markdown_cell(row_student_id(row)),
                    escape_markdown_cell(row_student_name(row)),
                    escape_markdown_cell(row.get("model_name")),
                    escape_markdown_cell(row.get("num_parameters")),
                    escape_markdown_cell(row.get("test_accuracy")),
                    escape_markdown_cell(row.get("test_macro_f1")),
                    escape_markdown_cell(row.get("efficiency_score")),
                    escape_markdown_cell(row.get("final_score")),
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
    parser.add_argument("--metrics", default=None, help="Path to metrics JSON.")
    parser.add_argument("--repo-root", default=None, help="Repository root override.")
    args = parser.parse_args()

    try:
        repo_root = Path(args.repo_root).resolve() if args.repo_root else repo_root_from_script()
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        metrics = (
            json.loads(Path(args.metrics).read_text(encoding="utf-8"))
            if args.metrics
            else None
        )
        log_path = repo_root / "leaderboard" / "submissions_log.csv"
        latest_markdown_path = repo_root / "leaderboard" / "latest_submissions.md"

        if args.status == "accepted":
            archive_latest(repo_root, Path(args.work_dir), metadata, metrics)

        append_log_row(log_path, metadata, args.status, args.message, metrics)
        regenerate_latest_markdown(log_path, latest_markdown_path)
    except Exception as exc:
        print(f"Could not update submission index: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
