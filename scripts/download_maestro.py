"""
Download MAESTRO dataset (optional - large download).

The MAESTRO dataset contains ~200 hours of piano performances
with aligned MIDI and audio from the International Piano-e-Competition.
"""

import argparse
import os
from pathlib import Path
import urllib.request
import zipfile
import json


MAESTRO_VERSIONS = {
    "v3.0.0": {
        "midi_only": "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0-midi.zip",
        "full": "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0.zip",
        "metadata": "https://storage.googleapis.com/magentadata/datasets/maestro/v3.0.0/maestro-v3.0.0.json"
    }
}


def download_file(url: str, output_path: Path):
    """Download a file with progress indication."""
    print(f"Downloading from {url}")
    print(f"Saving to {output_path}")

    def reporthook(count, block_size, total_size):
        percent = int(count * block_size * 100 / total_size)
        print(f"\rProgress: {percent}%", end='', flush=True)

    urllib.request.urlretrieve(url, output_path, reporthook)
    print("\nDownload complete!")


def download_maestro(
    output_dir: str = "data/raw/maestro",
    version: str = "v3.0.0",
    midi_only: bool = True
):
    """
    Download MAESTRO dataset.

    Args:
        output_dir: Directory to save the dataset
        version: Dataset version (default: v3.0.0)
        midi_only: If True, download only MIDI files (~100MB).
                   If False, download full dataset with audio (~100GB)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    if version not in MAESTRO_VERSIONS:
        print(f"Error: Version {version} not found.")
        print(f"Available versions: {list(MAESTRO_VERSIONS.keys())}")
        return

    dataset_info = MAESTRO_VERSIONS[version]

    if midi_only:
        print("Downloading MIDI-only version (~100 MB)")
        url = dataset_info["midi_only"]
        zip_filename = "maestro-midi.zip"
    else:
        print("WARNING: Downloading full dataset with audio (~100 GB)")
        response = input("This is a very large download. Continue? (yes/no): ")
        if response.lower() != "yes":
            print("Download cancelled.")
            return
        url = dataset_info["full"]
        zip_filename = "maestro-full.zip"

    zip_path = output_path / zip_filename

    if zip_path.exists():
        print(f"File {zip_path} already exists.")
        response = input("Re-download? (yes/no): ")
        if response.lower() != "yes":
            print("Skipping download.")
        else:
            download_file(url, zip_path)
    else:
        download_file(url, zip_path)

    print(f"\nExtracting {zip_path}...")
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(output_path)

    print(f"✓ Dataset extracted to {output_path}")

    metadata_url = dataset_info["metadata"]
    metadata_path = output_path / "maestro-metadata.json"
    if not metadata_path.exists():
        print(f"\nDownloading metadata...")
        download_file(metadata_url, metadata_path)

        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        print(f"✓ Metadata downloaded: {len(metadata)} entries")


def main():
    parser = argparse.ArgumentParser(
        description="Download MAESTRO classical piano dataset"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw/maestro",
        help="Output directory for dataset"
    )
    parser.add_argument(
        "--version",
        type=str,
        default="v3.0.0",
        help="Dataset version"
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Download full dataset with audio (~100GB). Default is MIDI-only (~100MB)"
    )

    args = parser.parse_args()

    download_maestro(
        output_dir=args.output_dir,
        version=args.version,
        midi_only=not args.full
    )


if __name__ == "__main__":
    main()
