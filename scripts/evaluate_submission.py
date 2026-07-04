#!/usr/bin/env python3
"""Evaluate predictions against hidden labels."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd


NUM_CLASSES = 5
REFERENCE_EFFICIENCY_PARAMS = 100_000


def read_predictions(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(f"predictions file not found: {path}")
    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    if list(df.columns) != ["id", "y_pred"]:
        raise ValueError("predictions.csv must contain exactly these columns: id,y_pred.")
    df["id"] = df["id"].astype(str).str.strip()
    df["y_pred"] = df["y_pred"].astype(str).str.strip().astype(int)
    return df


def read_labels(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise ValueError(
            f"Hidden label file not found at {path}. Add it to the private evaluator "
            "environment or configure the workflow to download it before evaluation."
        )

    df = pd.read_csv(path, dtype=str, keep_default_na=False, encoding="utf-8-sig")
    required_columns = {"id", "label"}
    missing = sorted(required_columns - set(df.columns))
    if missing:
        raise ValueError(f"Hidden labels are missing required columns: {', '.join(missing)}.")

    df = df[["id", "label"]].copy()
    df["id"] = df["id"].astype(str).str.strip()
    df["label"] = df["label"].astype(str).str.strip().astype(int)

    if df["id"].eq("").any():
        raise ValueError("Hidden labels contain missing IDs.")
    if df["id"].duplicated().any():
        raise ValueError("Hidden labels contain duplicated IDs.")

    return df


def require_exact_id_match(predictions: pd.DataFrame, labels: pd.DataFrame) -> None:
    predicted_ids = set(predictions["id"])
    label_ids = set(labels["id"])

    missing_ids = sorted(label_ids - predicted_ids)
    extra_ids = sorted(predicted_ids - label_ids)
    if missing_ids or extra_ids:
        parts = []
        if missing_ids:
            parts.append(f"missing test IDs: {', '.join(missing_ids[:5])}")
        if extra_ids:
            parts.append(f"unknown test IDs: {', '.join(extra_ids[:5])}")
        raise ValueError("predictions.csv does not match the hidden test IDs; " + "; ".join(parts))


def macro_f1_score(y_true: list[int], y_pred: list[int]) -> float:
    per_class_f1 = []

    for class_id in range(NUM_CLASSES):
        true_positive = sum(yt == class_id and yp == class_id for yt, yp in zip(y_true, y_pred))
        false_positive = sum(yt != class_id and yp == class_id for yt, yp in zip(y_true, y_pred))
        false_negative = sum(yt == class_id and yp != class_id for yt, yp in zip(y_true, y_pred))

        precision_denominator = true_positive + false_positive
        recall_denominator = true_positive + false_negative
        precision = true_positive / precision_denominator if precision_denominator else 0.0
        recall = true_positive / recall_denominator if recall_denominator else 0.0
        f1_denominator = precision + recall
        per_class_f1.append(2 * precision * recall / f1_denominator if f1_denominator else 0.0)

    return sum(per_class_f1) / NUM_CLASSES


def efficiency_score(num_parameters: int) -> float:
    """Parameter efficiency without an upper parameter limit."""

    if num_parameters <= 0:
        raise ValueError("num_parameters must be positive.")
    return min(1.0, REFERENCE_EFFICIENCY_PARAMS / num_parameters)


def evaluate(predictions_path: Path, labels_path: Path, metadata_path: Path) -> dict:
    predictions = read_predictions(predictions_path)
    labels = read_labels(labels_path)
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))

    require_exact_id_match(predictions, labels)
    merged = labels.merge(predictions, on="id", how="left", validate="one_to_one")

    y_true = merged["label"].astype(int).tolist()
    y_pred = merged["y_pred"].astype(int).tolist()
    accuracy = sum(yt == yp for yt, yp in zip(y_true, y_pred)) / len(y_true)
    macro_f1 = macro_f1_score(y_true, y_pred)
    efficiency = efficiency_score(int(metadata["num_parameters"]))
    final_score = (0.70 * macro_f1) + (0.20 * accuracy) + (0.10 * efficiency)

    return {
        "num_test_examples": len(y_true),
        "accuracy": round(accuracy, 6),
        "macro_f1": round(macro_f1, 6),
        "efficiency_score": round(efficiency, 6),
        "final_score": round(final_score, 6),
        "efficiency_rule": (
            f"min(1.0, {REFERENCE_EFFICIENCY_PARAMS} / num_parameters); "
            "there is no upper parameter limit"
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions", required=True, help="Path to predictions.csv.")
    parser.add_argument("--labels", required=True, help="Path to hidden test labels CSV.")
    parser.add_argument("--metadata", required=True, help="Path to metadata JSON.")
    parser.add_argument("--output", required=True, help="Where to write metrics JSON.")
    args = parser.parse_args()

    try:
        metrics = evaluate(Path(args.predictions), Path(args.labels), Path(args.metadata))
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(metrics, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    except Exception as exc:
        print(f"Evaluation failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
