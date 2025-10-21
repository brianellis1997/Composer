# Classical MIDI Datasets for Composer Project

## Overview
This document catalogs available classical MIDI datasets suitable for training/fine-tuning music generation models.

## Primary Datasets

### 1. HuggingFace: drengskapur/midi-classical-music - **RECOMMENDED**
**URL**: https://huggingface.co/datasets/drengskapur/midi-classical-music

**Pros**:
- Organized by composer (perfect for our use case)
- Easy integration with HuggingFace datasets library
- Includes major classical composers (Bach, Mozart, Beethoven, Chopin, etc.)
- Direct download via Python
- Quality curated collection

**Cons**:
- Size may vary per composer
- Need to verify data quality

**Usage**:
```python
from datasets import load_dataset
dataset = load_dataset("drengskapur/midi-classical-music")
```

### 2. Kunstderfuge
**URL**: https://www.kunstderfuge.com/

**Details**:
- 19,300+ classical MIDI files
- License: CC BY-NC-SA (non-commercial with attribution)
- Comprehensive collection including:
  - Complete piano works by Beethoven, Chopin, Haydn, Mozart
  - Bach complete works
  - Original piano rolls
- Well-organized by composer and opus

**Pros**:
- Massive collection
- High quality human curation
- Includes rare/complete works
- Free for research/educational use

**Cons**:
- Manual download required
- CC BY-NC-SA license (non-commercial)
- May need cleanup/validation

### 3. Piano-MIDI.de
**URL**: http://piano-midi.de/

**Details**:
- Classical piano MIDI and MP3 sequences
- Major composers: Bach, Beethoven, Brahms, Chopin, Debussy, Grieg, Haydn, Liszt, Mozart, Mussorgsky, Schubert, Schumann, Tchaikovsky

**Pros**:
- High quality piano transcriptions
- Free download
- Focus on piano (good for our initial scope)

**Cons**:
- Smaller than Kunstderfuge
- Manual collection required

### 4. MAESTRO Dataset
**URL**: https://magenta.tensorflow.org/datasets/maestro

**Details**:
- 200+ hours of aligned MIDI and audio
- 10,855 unique solo piano works
- 2,786 composers
- From International Piano-e-Competition
- 62 major composers

**Pros**:
- High quality performance MIDI
- Audio-aligned (useful for future multimodal work)
- Academic standard dataset
- Extensive metadata

**Cons**:
- Very large download (>100GB with audio)
- May contain modern pieces, not just classical
- Performance MIDI vs score MIDI (timing variations)

**License**: CC BY-NC-SA 4.0

### 5. GiantMIDI-Piano
**URL**: https://github.com/bytedance/GiantMIDI-Piano

**Details**:
- 10,855 unique solo piano works
- 2,786 composers
- 38.7 million transcribed notes
- Focuses on classical piano music

**Pros**:
- Massive scale
- Academic research quality
- Extensive composer coverage

**Cons**:
- Transcribed from audio (may have quality issues)
- Very large dataset
- Computational requirements for full dataset

### 6. GigaMIDI (HuggingFace)
**URL**: https://huggingface.co/datasets/Metacreation/GigaMIDI

**Details**:
- 2.1 million+ unique MIDI files
- Comprehensive multi-genre collection
- Loop detection annotations
- 9.2M+ non-expressive loops
- 2.3M+ expressive loops

**Pros**:
- Largest available MIDI collection
- HuggingFace integration
- Good for pre-training

**Cons**:
- Mixed genres (not classical-only)
- Requires filtering for classical content
- Extremely large scale

## Dataset Recommendations by Use Case

### Initial Experiments (Crawl Stage)
**Recommended**: Piano-MIDI.de + HuggingFace drengskapur/midi-classical-music
- Manageable size
- High quality
- Easy to download and process
- Good composer variety

### Composer-Specific Fine-tuning (Walk Stage)
**Recommended**: Kunstderfuge subset
- Filter by specific composer (e.g., all Bach works)
- Complete works available
- High quality curation

### Large-Scale Pre-training (Run Stage)
**Recommended**: MAESTRO + GiantMIDI-Piano
- Academic quality
- Massive scale
- Good for foundation model training

## Target Composers for Initial Development

### Tier 1 (Start Here)
1. **J.S. Bach** - Well-structured, polyphonic, lots of available data
2. **Mozart** - Classical period, clear structure, melodic
3. **Beethoven** - Romantic transition, varied styles

### Tier 2 (Expansion)
4. **Chopin** - Romantic piano specialist
5. **Rachmaninoff** - Complex harmonies, technical virtuosity

## Data Processing Considerations

### MIDI Format Types
- **Score MIDI**: Clean, quantized, score-accurate
- **Performance MIDI**: Expressive timing, dynamics, pedaling

**Recommendation**: Start with score MIDI for structure learning, add performance MIDI later.

### Data Cleaning Needs
1. Tempo normalization
2. Key signature standardization
3. Instrument filtering (piano focus)
4. Length filtering (too short/long sequences)
5. Quality validation (corrupted files)

### Sequence Length Considerations
- M1 Pro 16GB RAM limits:
  - Estimate: ~2000-4000 token sequences comfortably
  - May need to chunk longer pieces
  - Sliding window approach for long compositions

## Next Steps
1. Download small test set from Piano-MIDI.de (Bach + Mozart)
2. Load HuggingFace drengskapur/midi-classical-music dataset
3. Analyze MIDI statistics (note distributions, lengths, etc.)
4. Create preprocessing pipeline
5. Build validation/test splits by composer
