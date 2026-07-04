#!/usr/bin/env python3
"""Download the two submitted files without executing student code."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import requests


FILES = {
    "predictions_csv_url": "predictions.csv",
    "ablations_md_url": "ABLATIONS.md",
}

MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
TIMEOUT_SECONDS = 30


def download(url: str, destination: Path) -> None:
    headers = {"User-Agent": "nayarit-challenge-submission-validator/1.0"}
    with requests.get(
        url,
        headers=headers,
        timeout=TIMEOUT_SECONDS,
        allow_redirects=True,
        stream=True,
    ) as response:
        response.raise_for_status()
        total = 0
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as output_file:
            for chunk in response.iter_content(chunk_size=64 * 1024):
                if not chunk:
                    continue
                total += len(chunk)
                if total > MAX_DOWNLOAD_BYTES:
                    raise ValueError(
                        f"{destination.name} is larger than "
                        f"{MAX_DOWNLOAD_BYTES // (1024 * 1024)} MB."
                    )
                output_file.write(chunk)

    if destination.stat().st_size == 0:
        raise ValueError(f"{destination.name} downloaded as an empty file.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, help="Path to metadata JSON.")
    parser.add_argument("--output-dir", required=True, help="Directory for downloads.")
    args = parser.parse_args()

    try:
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        output_dir = Path(args.output_dir)
        for url_key, filename in FILES.items():
            url = metadata.get(url_key)
            if not url:
                raise ValueError(f"metadata is missing {url_key}.")
            download(url, output_dir / filename)
    except requests.HTTPError as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

