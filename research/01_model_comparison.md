# Model Comparison for Composer Project

## Overview
This document compares pre-trained transformer models suitable for fine-tuning on classical MIDI music generation.

## Model Options

### 1. SkyTNT MIDI Model (HuggingFace) - **RECOMMENDED**
**Status**: Active (2024), Open Source
**Repository**: https://huggingface.co/skytnt/midi-model
**GitHub**: https://github.com/SkyTNT/midi-model

**Pros**:
- Recent release (2024) with active maintenance
- Native HuggingFace integration
- Designed specifically for MIDI event-based generation
- Transformer architecture optimized for symbolic music
- Easy fine-tuning support
- Good documentation and community support

**Cons**:
- Smaller community compared to larger models
- Limited published benchmarks on classical music specifically

**Technical Details**:
- Event-based MIDI tokenization
- Transformer decoder architecture
- Supports conditional generation
- Can handle long sequences efficiently

### 2. MusicGen (Meta AI)
**Status**: Active, Open Source (with restrictions)
**Repository**: https://huggingface.co/facebook/musicgen

**License**:
- Code: MIT License
- Pre-trained weights: CC-BY-NC 4.0 (non-commercial only)

**Pros**:
- State-of-the-art audio generation quality
- Strong Meta AI backing and research
- LoRA fine-tuning support for efficient adaptation
- Can fine-tune with 9-10 tracks in ~15 minutes on good hardware
- HuggingFace transformers integration (v4.31.0+)

**Cons**:
- Non-commercial license on weights (research/personal use only)
- Generates raw audio, not MIDI (different use case than our needs)
- Higher computational requirements
- Designed for audio, not symbolic music

**Verdict**: Not ideal for our MIDI-focused classical music project due to audio generation focus.

### 3. Google Music Transformer (Magenta)
**Status**: Open Source, legacy codebase
**Repository**: https://github.com/magenta/magenta

**Pros**:
- Well-established research foundation
- Proven success on classical music (trained on MAESTRO)
- Open source and free to use
- Relative positional encoding for music structure

**Cons**:
- TensorFlow 1.x based (outdated)
- Requires TFRecord format conversion
- More complex fine-tuning pipeline
- Less active development compared to newer alternatives
- Harder to integrate with modern PyTorch workflows

**Verdict**: Good historical reference, but outdated for new projects.

### 4. MidiBERT
**Status**: Research model, available
**Paper**: https://arxiv.org/abs/2107.05223

**Pros**:
- BERT-like pre-training specifically for MIDI
- Supports both score and performance MIDI
- Fine-tuning for classification and generation tasks
- Academic validation

**Cons**:
- Primarily designed for classification, not generation
- Less straightforward for generative tasks
- Limited community adoption
- May require more custom implementation

**Verdict**: Better suited for analysis/classification than generation.

### 5. GPT-2 for Music (Community Implementations)
**Status**: Various community implementations
**Example**: HuggingFace tutorials on MIDI-GPT

**Pros**:
- Leverage powerful GPT-2 architecture
- Well-understood training procedures
- HuggingFace integration
- Can convert MIDI to token sequences

**Cons**:
- Requires custom MIDI tokenization scheme
- Not pre-trained on music (unless using fine-tuned versions)
- Less specialized than music-specific models

**Verdict**: Good fallback option if SkyTNT doesn't meet needs.

## Recommendation

**Primary Choice: SkyTNT MIDI Model**

Reasons:
1. **Modern and Active**: 2024 release with ongoing support
2. **Purpose-Built**: Specifically designed for MIDI generation
3. **Easy Integration**: Native HuggingFace support
4. **MIDI Focus**: Symbolic music representation aligns with our use case
5. **Fine-tuning Ready**: Straightforward adaptation to classical composers

**Backup Choice: GPT-2 for Music**
- If SkyTNT doesn't meet performance expectations
- More established architecture with proven scaling

## Next Steps
1. Test SkyTNT model inference on M1 Pro
2. Benchmark generation quality and speed
3. Evaluate memory requirements
4. Test fine-tuning pipeline on small classical dataset
5. Compare outputs with Compose_and_Embellish baseline
