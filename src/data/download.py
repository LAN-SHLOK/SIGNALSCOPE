"""
SignalScope — Dataset & Benchmark Download Utility (Role 5)
Handles downloading, checksum verification, and extraction of training and validation datasets.
"""
import os
import sys
import hashlib
import zipfile
import tarfile
import urllib.request
from pathlib import Path
from typing import Optional, Dict

logger_initialized = False


def compute_sha256(file_path: Path) -> str:
    """Compute SHA256 hash of a local file."""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192 * 1024):
            sha256.update(chunk)
    return sha256.hexdigest()


def download_file(
    url: str,
    dest_path: Path,
    expected_sha256: Optional[str] = None,
    chunk_size: int = 1024 * 1024
) -> Path:
    """Download a file with progress reporting and optional SHA256 verification."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    
    if dest_path.exists() and expected_sha256:
        if compute_sha256(dest_path) == expected_sha256:
            print(f"[OK] File already exists and verified: {dest_path.name}")
            return dest_path

    print(f"Downloading {url} -> {dest_path}...")
    with urllib.request.urlopen(url) as response, open(dest_path, "wb") as out_file:
        total_size = int(response.info().get("Content-Length", 0))
        downloaded = 0
        while chunk := response.read(chunk_size):
            out_file.write(chunk)
            downloaded += len(chunk)
            if total_size > 0:
                pct = (downloaded / total_size) * 100
                print(f"\rProgress: {pct:.1f}% ({downloaded // (1024*1024)}MB / {total_size // (1024*1024)}MB)", end="")
    print("\nDownload complete.")

    if expected_sha256:
        actual = compute_sha256(dest_path)
        if actual != expected_sha256:
            raise ValueError(f"Checksum mismatch! Expected {expected_sha256}, got {actual}")
        print("[OK] Checksum verified.")

    return dest_path


def extract_archive(archive_path: Path, extract_to: Path) -> Path:
    """Extract .zip or .tar.gz archive safely."""
    extract_to.mkdir(parents=True, exist_ok=True)
    print(f"Extracting {archive_path.name} to {extract_to}...")
    
    if archive_path.suffix == ".zip":
        with zipfile.ZipFile(archive_path, "r") as z:
            z.extractall(extract_to)
    elif archive_path.name.endswith((".tar.gz", ".tgz", ".tar")):
        with tarfile.open(archive_path, "r:*") as t:
            t.extractall(extract_to)
    else:
        raise ValueError(f"Unsupported archive format: {archive_path.name}")
        
    print("Extraction complete.")
    return extract_to


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SignalScope Dataset Downloader")
    parser.add_argument("--url", type=str, required=True, help="URL of archive to download")
    parser.add_argument("--dest", type=str, default="data/raw/", help="Destination directory")
    parser.add_argument("--sha256", type=str, default=None, help="Expected SHA256 checksum")
    parser.add_argument("--extract", action="store_true", help="Extract archive after download")
    args = parser.parse_args()

    dest_dir = Path(args.dest)
    filename = args.url.split("/")[-1].split("?")[0]
    archive_dest = dest_dir / filename

    dl_path = download_file(args.url, archive_dest, expected_sha256=args.sha256)
    if args.extract:
        extract_archive(dl_path, dest_dir / dl_path.stem)
