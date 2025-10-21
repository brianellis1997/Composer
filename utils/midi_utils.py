"""
MIDI file utilities for loading, validation, and basic processing.
"""

from pathlib import Path
from typing import Dict, List, Optional, Union
import miditoolkit
import pretty_midi
import numpy as np


def load_midi_file(
    file_path: Union[str, Path],
    backend: str = "miditoolkit"
) -> Union[miditoolkit.MidiFile, pretty_midi.PrettyMIDI]:
    """
    Load a MIDI file using specified backend.

    Args:
        file_path: Path to MIDI file
        backend: Either 'miditoolkit' or 'pretty_midi'

    Returns:
        Loaded MIDI object

    Raises:
        ValueError: If backend is not recognized
        FileNotFoundError: If MIDI file doesn't exist
    """
    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"MIDI file not found: {file_path}")

    if backend == "miditoolkit":
        return miditoolkit.MidiFile(str(file_path))
    elif backend == "pretty_midi":
        return pretty_midi.PrettyMIDI(str(file_path))
    else:
        raise ValueError(f"Unknown backend: {backend}. Use 'miditoolkit' or 'pretty_midi'")


def get_midi_info(midi_file: Union[str, Path, miditoolkit.MidiFile, pretty_midi.PrettyMIDI]) -> Dict:
    """
    Extract basic information from a MIDI file.

    Args:
        midi_file: Path to MIDI file or loaded MIDI object

    Returns:
        Dictionary with MIDI file information
    """
    if isinstance(midi_file, (str, Path)):
        midi = load_midi_file(midi_file, backend="miditoolkit")
    else:
        midi = midi_file

    if isinstance(midi, miditoolkit.MidiFile):
        return _get_info_miditoolkit(midi)
    elif isinstance(midi, pretty_midi.PrettyMIDI):
        return _get_info_pretty_midi(midi)
    else:
        raise ValueError(f"Unknown MIDI type: {type(midi)}")


def _get_info_miditoolkit(midi: miditoolkit.MidiFile) -> Dict:
    """Get info from miditoolkit MIDI object."""
    info = {
        "ticks_per_beat": midi.ticks_per_beat,
        "tempo_changes": len(midi.tempo_changes),
        "time_signature_changes": len(midi.time_signature_changes),
        "key_signature_changes": len(midi.key_signature_changes),
        "instruments": []
    }

    for inst in midi.instruments:
        inst_info = {
            "program": inst.program,
            "is_drum": inst.is_drum,
            "name": inst.name,
            "num_notes": len(inst.notes)
        }
        info["instruments"].append(inst_info)

    total_notes = sum(len(inst.notes) for inst in midi.instruments)
    info["total_notes"] = total_notes

    if midi.instruments:
        all_notes = []
        for inst in midi.instruments:
            all_notes.extend([note.pitch for note in inst.notes])

        if all_notes:
            info["pitch_range"] = {
                "min": min(all_notes),
                "max": max(all_notes),
                "span": max(all_notes) - min(all_notes)
            }

    if midi.max_tick:
        if midi.tempo_changes:
            avg_tempo = np.mean([tc.tempo for tc in midi.tempo_changes])
            duration_seconds = (midi.max_tick / midi.ticks_per_beat) * (60 / avg_tempo)
            info["duration_seconds"] = duration_seconds
            info["duration_ticks"] = midi.max_tick

    return info


def _get_info_pretty_midi(midi: pretty_midi.PrettyMIDI) -> Dict:
    """Get info from pretty_midi object."""
    info = {
        "duration_seconds": midi.get_end_time(),
        "instruments": []
    }

    for inst in midi.instruments:
        inst_info = {
            "program": inst.program,
            "is_drum": inst.is_drum,
            "name": inst.name,
            "num_notes": len(inst.notes)
        }
        info["instruments"].append(inst_info)

    total_notes = sum(len(inst.notes) for inst in midi.instruments)
    info["total_notes"] = total_notes

    if midi.instruments:
        all_notes = []
        for inst in midi.instruments:
            all_notes.extend([note.pitch for note in inst.notes])

        if all_notes:
            info["pitch_range"] = {
                "min": min(all_notes),
                "max": max(all_notes),
                "span": max(all_notes) - min(all_notes)
            }

    return info


def validate_midi_file(
    file_path: Union[str, Path],
    min_notes: int = 10,
    max_duration: Optional[float] = None,
    min_duration: Optional[float] = None,
    require_tempo: bool = False
) -> tuple[bool, str]:
    """
    Validate a MIDI file against quality criteria.

    Args:
        file_path: Path to MIDI file
        min_notes: Minimum number of notes required
        max_duration: Maximum duration in seconds (None for no limit)
        min_duration: Minimum duration in seconds (None for no limit)
        require_tempo: Whether tempo changes are required

    Returns:
        Tuple of (is_valid, reason)
    """
    try:
        info = get_midi_info(file_path)

        if info["total_notes"] < min_notes:
            return False, f"Too few notes: {info['total_notes']} < {min_notes}"

        if "duration_seconds" in info:
            duration = info["duration_seconds"]

            if max_duration and duration > max_duration:
                return False, f"Duration too long: {duration:.1f}s > {max_duration}s"

            if min_duration and duration < min_duration:
                return False, f"Duration too short: {duration:.1f}s < {min_duration}s"

        if require_tempo and info.get("tempo_changes", 0) == 0:
            return False, "No tempo changes found"

        return True, "Valid"

    except Exception as e:
        return False, f"Error loading MIDI: {str(e)}"


def filter_midi_by_instrument(
    midi_file: Union[str, Path],
    program_numbers: Optional[List[int]] = None,
    exclude_drums: bool = True
) -> miditoolkit.MidiFile:
    """
    Filter MIDI file to keep only specific instruments.

    Args:
        midi_file: Path to MIDI file or loaded MidiFile
        program_numbers: List of MIDI program numbers to keep (None = keep all)
                        Piano is typically 0-7
        exclude_drums: Whether to exclude drum tracks

    Returns:
        Filtered MidiFile object
    """
    if isinstance(midi_file, (str, Path)):
        midi = load_midi_file(midi_file, backend="miditoolkit")
    else:
        midi = midi_file

    filtered_instruments = []

    for inst in midi.instruments:
        if exclude_drums and inst.is_drum:
            continue

        if program_numbers is None or inst.program in program_numbers:
            filtered_instruments.append(inst)

    midi.instruments = filtered_instruments

    return midi


def get_piano_midi(midi_file: Union[str, Path]) -> miditoolkit.MidiFile:
    """
    Extract only piano tracks from a MIDI file.

    Piano programs: 0-7 in General MIDI
    - 0: Acoustic Grand Piano
    - 1: Bright Acoustic Piano
    - 2: Electric Grand Piano
    - 3: Honky-tonk Piano
    - 4: Electric Piano 1
    - 5: Electric Piano 2
    - 6: Harpsichord
    - 7: Clavinet

    Args:
        midi_file: Path to MIDI file

    Returns:
        MidiFile with only piano tracks
    """
    piano_programs = list(range(8))
    return filter_midi_by_instrument(midi_file, program_numbers=piano_programs)


def midi_to_note_sequence(midi: miditoolkit.MidiFile) -> List[Dict]:
    """
    Convert MIDI to a list of note dictionaries.

    Args:
        midi: MidiFile object

    Returns:
        List of note dictionaries with keys: pitch, start, end, velocity
    """
    notes = []

    for inst in midi.instruments:
        for note in inst.notes:
            notes.append({
                "pitch": note.pitch,
                "start": note.start,
                "end": note.end,
                "velocity": note.velocity,
                "instrument": inst.program
            })

    notes.sort(key=lambda x: x["start"])

    return notes


def print_midi_summary(file_path: Union[str, Path]):
    """
    Print a human-readable summary of a MIDI file.

    Args:
        file_path: Path to MIDI file
    """
    info = get_midi_info(file_path)

    print(f"\nMIDI File: {Path(file_path).name}")
    print("=" * 60)

    if "duration_seconds" in info:
        duration = info["duration_seconds"]
        print(f"Duration: {duration:.2f}s ({duration/60:.2f} minutes)")

    if "duration_ticks" in info:
        print(f"Total ticks: {info['duration_ticks']}")
        print(f"Ticks per beat: {info['ticks_per_beat']}")

    print(f"Total notes: {info['total_notes']}")

    if "pitch_range" in info:
        pr = info["pitch_range"]
        print(f"Pitch range: {pr['min']} to {pr['max']} (span: {pr['span']})")

    print(f"Tempo changes: {info.get('tempo_changes', 'N/A')}")
    print(f"Time signature changes: {info.get('time_signature_changes', 'N/A')}")
    print(f"Key signature changes: {info.get('key_signature_changes', 'N/A')}")

    print(f"\nInstruments ({len(info['instruments'])}):")
    for i, inst in enumerate(info["instruments"], 1):
        drum_str = " [DRUM]" if inst["is_drum"] else ""
        print(f"  {i}. Program {inst['program']}: {inst['name']}{drum_str} ({inst['num_notes']} notes)")
