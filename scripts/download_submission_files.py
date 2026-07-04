#!/usr/bin/env python3
"""Download and extract the submitted ZIP without executing student code."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from zipfile import BadZipFile, ZipFile

import requests


MAX_DOWNLOAD_BYTES = 25 * 1024 * 1024
TIMEOUT_SECONDS = 30
REQUIRED_ZIP_FILES = {
    "predictions.csv": "predictions.csv",
    "ABLATIONS.md": "ABLATIONS.md",
}


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


def extract_required_files(zip_path: Path, output_dir: Path) -> None:
    try:
        with ZipFile(zip_path) as archive:
            matches: dict[str, object] = {}
            for info in archive.infolist():
                if info.is_dir():
                    continue
                filename = Path(info.filename.replace("\\", "/")).name
                if filename not in REQUIRED_ZIP_FILES:
                    continue
                if filename in matches:
                    raise ValueError(f"submission.zip contains multiple {filename} files.")
                if info.file_size > MAX_DOWNLOAD_BYTES:
                    raise ValueError(
                        f"{filename} inside submission.zip is larger than "
                        f"{MAX_DOWNLOAD_BYTES // (1024 * 1024)} MB."
                    )
                matches[filename] = info

            missing = sorted(set(REQUIRED_ZIP_FILES) - set(matches))
            if missing:
                raise ValueError(
                    "submission.zip is missing required file(s): " + ", ".join(missing)
                )

            output_dir.mkdir(parents=True, exist_ok=True)
            for filename, destination_name in REQUIRED_ZIP_FILES.items():
                destination = output_dir / destination_name
                with archive.open(matches[filename]) as source, destination.open("wb") as output:
                    shutil.copyfileobj(source, output)
                if destination.stat().st_size == 0:
                    raise ValueError(f"{destination_name} inside submission.zip is empty.")
    except BadZipFile as exc:
        raise ValueError("submission.zip is not a valid ZIP file.") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", required=True, help="Path to metadata JSON.")
    parser.add_argument("--output-dir", required=True, help="Directory for downloads.")
    args = parser.parse_args()

    try:
        metadata = json.loads(Path(args.metadata).read_text(encoding="utf-8"))
        output_dir = Path(args.output_dir)
        url = metadata.get("submission_zip_url")
        if not url:
            raise ValueError("metadata is missing submission_zip_url.")
        zip_path = output_dir / "submission.zip"
        download(url, zip_path)
        extract_required_files(zip_path, output_dir)
    except requests.HTTPError as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Download failed: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
