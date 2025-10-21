"""
Download classical MIDI dataset from HuggingFace.

This script downloads the drengskapur/midi-classical-music dataset
which is organized by composer.
"""

import os
from pathlib import Path
from datasets import load_dataset
import argparse


def download_hf_classical_midi(output_dir: str = "data/raw/hf_classical"):
    """
    Download HuggingFace classical MIDI dataset.

    Args:
        output_dir: Directory to save the downloaded MIDI files
    """
    print("Downloading HuggingFace classical MIDI dataset...")
    print(f"Output directory: {output_dir}")

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    try:
        dataset = load_dataset("drengskapur/midi-classical-music")

        print(f"\nDataset loaded successfully!")
        print(f"Dataset structure: {dataset}")

        if hasattr(dataset, 'keys'):
            print(f"\nSplits: {list(dataset.keys())}")
            for split_name in dataset.keys():
                print(f"\n{split_name} split:")
                print(f"  Number of examples: {len(dataset[split_name])}")
                if len(dataset[split_name]) > 0:
                    print(f"  Features: {dataset[split_name].features}")
                    print(f"  First example keys: {dataset[split_name][0].keys()}")

        save_path = output_path / "dataset_cache"
        dataset.save_to_disk(str(save_path))
        print(f"\nDataset saved to: {save_path}")

        return dataset

    except Exception as e:
        print(f"Error downloading dataset: {e}")
        print("\nNote: This dataset may require authentication or may not be available.")
        print("Alternative: Use manual download from Kunstderfuge or Piano-MIDI.de")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Download classical MIDI dataset from HuggingFace"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data/raw/hf_classical",
        help="Output directory for downloaded data"
    )

    args = parser.parse_args()

    dataset = download_hf_classical_midi(args.output_dir)

    if dataset:
        print("\n✓ Download completed successfully!")
    else:
        print("\n✗ Download failed. Please check error messages above.")


if __name__ == "__main__":
    main()
