# Composer

Fine-tuned on millions of bars of music from the greats, Composer is an app that allows you to generate new classical music in the style of classical artists (Bach, Mozart, Beethoven, Chopin, Rachmaninoff) as well as generate your own music based on a custom dataset. Utilizing the transformer architecture, Composer is able to compose music like ChatGPT composes words.

## Overview

Composer uses transformer-based neural networks to learn the musical patterns and styles of classical composers from MIDI files. Once trained, it can generate new compositions that capture the essence of these masters while creating entirely original pieces.

## Features (Planned)

- **Composer-Specific Generation**: Generate music in the style of Bach, Mozart, Beethoven, Chopin, and more
- **Custom Training**: Fine-tune on your own MIDI files to generate music in your personal style
- **MIDI-Based**: Works with symbolic music representation for precise note control
- **Efficient Fine-Tuning**: Uses LoRA (Low-Rank Adaptation) for resource-efficient training
- **M1 Pro Optimized**: Leverages Apple Silicon MPS (Metal Performance Shaders) for GPU acceleration

## Project Structure

```
composer/
├── data/              # MIDI datasets (gitignored)
│   ├── raw/           # Downloaded datasets
│   └── processed/     # Preprocessed data
├── models/            # Model implementations and checkpoints
│   ├── checkpoints/   # Training checkpoints
│   └── pretrained/    # Pre-trained models
├── notebooks/         # Jupyter notebooks for exploration
│   ├── 01_midi_exploration.ipynb
│   └── 02_model_baseline.ipynb
├── research/          # Research documentation
│   ├── 01_model_comparison.md
│   ├── 02_dataset_analysis.md
│   └── 03_compute_requirements.md
├── scripts/           # Data download and training scripts
│   ├── download_hf_dataset.py
│   └── download_maestro.py
└── utils/             # Helper functions
    └── midi_utils.py
```

## Setup

### Prerequisites

- macOS 12.3+ (for MPS support) or Linux/Windows with CUDA
- Conda (miniconda or anaconda)
- Python 3.12

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Composer.git
cd Composer
```

2. Create and activate the conda environment:
```bash
conda create -n composer python=3.12 -y
conda activate composer
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Quick Start

### 1. Download Data

Download a small classical MIDI dataset:
```bash
python scripts/download_hf_dataset.py
```

For the larger MAESTRO dataset (MIDI-only, ~100MB):
```bash
python scripts/download_maestro.py --midi-only
```

### 2. Explore Data

Open the exploration notebook:
```bash
jupyter notebook notebooks/01_midi_exploration.ipynb
```

### 3. Test Baseline Model

Test the pre-trained model:
```bash
jupyter notebook notebooks/02_model_baseline.ipynb
```

## Development Phases

### Crawl Stage (Current)
- [x] Environment setup with conda
- [x] Research on models and datasets
- [x] Data download scripts
- [x] MIDI preprocessing utilities
- [x] Exploratory notebooks
- [ ] Baseline model testing on M1 Pro

### Walk Stage (Next)
- [ ] Composer-specific fine-tuning
- [ ] LoRA adapter implementation
- [ ] Evaluation metrics
- [ ] Generation quality assessment
- [ ] Multi-composer support

### Run Stage (Future)
- [ ] Large-scale training on cloud compute
- [ ] Web interface for music generation
- [ ] Model deployment
- [ ] Multi-task learning across composers

## Technical Details

### Model Architecture
- **Primary**: SkyTNT MIDI Model (transformer-based)
- **Backup**: GPT-2 adapted for music generation
- **Training**: LoRA fine-tuning for efficiency

### Datasets
- **HuggingFace**: drengskapur/midi-classical-music (organized by composer)
- **MAESTRO**: 200 hours of classical piano performances
- **Kunstderfuge**: 19,300+ classical MIDI files
- **Piano-MIDI.de**: High-quality piano transcriptions

### Hardware
- **Development**: MacBook M1 Pro (16GB RAM, MPS GPU)
- **Production Training**: Cloud GPU (A100/H100) for large-scale training

## Resources

- [Research Documentation](research/)
- [Previous Work: Compose and Embellish](../Compose_and_Embellish)
- [HuggingFace Transformers](https://huggingface.co/docs/transformers)
- [MAESTRO Dataset](https://magenta.tensorflow.org/datasets/maestro)

## License

[To be determined]

## Acknowledgments

- Inspired by OpenAI's MuseNet and Jukebox
- Built on HuggingFace Transformers
- Uses datasets from MAESTRO, Kunstderfuge, and community contributors

