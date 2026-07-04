#!/usr/bin/env python3
"""Validate predictions.csv and ABLATIONS.md."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = ["id", "y_pred"]
MIN_CLASS_ID = 0
MAX_CLASS_ID = 4


def validate_predictions(path: Path) -> None:
    if not path.exists():
        raise ValueError("predictions.csv does not exist.")

    try:
        df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    except Exception as exc:
        raise ValueError(f"predictions.csv could not be read as CSV: {exc}") from exc

    if list(df.columns) != EXPECTED_COLUMNS:
        raise ValueError(
            "predictions.csv must contain exactly two columns in this order: id,y_pred."
        )

    ids = df["id"].astype(str).str.strip()
    predictions = df["y_pred"].astype(str).str.strip()

    if ids.eq("").any():
        raise ValueError("predictions.csv contains missing IDs.")

    duplicated_ids = ids[ids.duplicated()].unique().tolist()
    if duplicated_ids:
        preview = ", ".join(duplicated_ids[:5])
        raise ValueError(f"predictions.csv contains duplicated IDs: {preview}.")

    if predictions.eq("").any():
        raise ValueError("predictions.csv contains missing predictions.")

    integer_mask = predictions.str.fullmatch(r"[+-]?\d+")
    if not bool(integer_mask.all()):
        bad_values = predictions[~integer_mask].unique().tolist()
        preview = ", ".join(bad_values[:5])
        raise ValueError(f"y_pred must be an integer. Invalid values: {preview}.")

    values = predictions.astype(int)
    range_mask = values.between(MIN_CLASS_ID, MAX_CLASS_ID)
    if not bool(range_mask.all()):
        bad_values = sorted({int(value) for value in values[~range_mask].tolist()})
        preview = ", ".join(str(value) for value in bad_values[:5])
        raise ValueError(
            f"y_pred must be between {MIN_CLASS_ID} and {MAX_CLASS_ID}. "
            f"Invalid values: {preview}."
        )


def validate_ablations(path: Path) -> None:
    if not path.exists():
        raise ValueError("ABLATIONS.md does not exist.")

    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.strip():
        raise ValueError("ABLATIONS.md is empty.")

    if not re.search(r"\b(Ablation|ablation|Experiment|experiment)\b", text):
        raise ValueError(
            "ABLATIONS.md should contain the word Ablation, ablation, "
            "Experiment, or experiment."
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, help="Path to predictions.csv.")
    parser.add_argument("--ablations", required=True, help="Path to ABLATIONS.md.")
    args = parser.parse_args()

    try:
        validate_predictions(Path(args.predictions))
        validate_ablations(Path(args.ablations))
    except Exception as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
