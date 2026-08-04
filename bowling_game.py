"""
bowling_game.py

Scoring library for a ten-pin bowling game. Same logic used in the
bowling-scorer project, copied here so this practice app is self-contained.
"""

from typing import List, Optional, Sequence

STRIKE_PINS = 10
NUM_FRAMES = 10


class InvalidGameError(ValueError):
    """Raised when the supplied game data is not a legal bowling game."""


def _parse_roll(symbol: str, previous_in_frame: Optional[int]) -> int:
    if not isinstance(symbol, str) or len(symbol) == 0:
        raise InvalidGameError(f"Invalid roll symbol: {symbol!r}")

    if symbol.upper() == "X":
        return STRIKE_PINS

    if symbol == "/":
        if previous_in_frame is None:
            raise InvalidGameError("A spare ('/') cannot be the first roll of a frame")
        return STRIKE_PINS - previous_in_frame

    if len(symbol) == 1 and symbol.isdigit():
        return int(symbol)

    raise InvalidGameError(f"Invalid roll symbol: {symbol!r}")


def _validate_frame_1_to_9(frame_num: int, symbols: Sequence[str], values: List[int]) -> None:
    if len(symbols) == 1:
        if values[0] != STRIKE_PINS:
            raise InvalidGameError(f"Frame {frame_num}: a single-roll frame must be a strike")
    elif len(symbols) == 2:
        first, second = values
        if first == STRIKE_PINS:
            raise InvalidGameError(f"Frame {frame_num}: a strike frame cannot have a second roll")
        if symbols[1] != "/" and (first + second) > STRIKE_PINS:
            raise InvalidGameError(f"Frame {frame_num}: total pins exceed 10 without a spare")
    else:
        raise InvalidGameError(
            f"Frame {frame_num}: must have 1 roll (strike) or 2 rolls, got {len(symbols)}"
        )


def _validate_frame_10(symbols: Sequence[str], values: List[int]) -> None:
    n = len(symbols)
    if n < 2 or n > 3:
        raise InvalidGameError(f"Frame 10: must have 2 or 3 rolls, got {n}")

    first = values[0]
    is_strike_start = first == STRIKE_PINS
    is_spare_pair = (not is_strike_start) and n >= 2 and (values[0] + values[1] == STRIKE_PINS)

    if is_strike_start:
        if n != 3:
            raise InvalidGameError(
                "Frame 10: a strike on the first roll must be followed by exactly two bonus rolls"
            )
        second_sym, third_sym = symbols[1], symbols[2]
        if second_sym == "/":
            raise InvalidGameError("Frame 10: a spare cannot follow a strike with no roll between")
        if second_sym.upper() != "X" and third_sym != "/":
            second_val, third_val = values[1], values[2]
            if second_val + third_val > STRIKE_PINS:
                raise InvalidGameError(
                    "Frame 10: bonus rolls after the strike exceed 10 pins without a spare"
                )
    elif is_spare_pair:
        if symbols[1] != "/":
            raise InvalidGameError(
                "Frame 10: two rolls totaling 10 must use '/' notation for the second roll"
            )
        if n != 3:
            raise InvalidGameError(
                "Frame 10: a spare in the first two rolls must be followed by exactly one bonus roll"
            )
    else:
        if n != 2:
            raise InvalidGameError("Frame 10: no bonus roll is allowed after an open frame")
        if values[0] + values[1] > STRIKE_PINS:
            raise InvalidGameError("Frame 10: total pins exceed 10 without a spare")


def _validate_and_flatten(frames: Sequence[Sequence[str]]):
    if frames is None or len(frames) != NUM_FRAMES:
        raise InvalidGameError(f"A game must have exactly {NUM_FRAMES} frames")

    flat_values: List[int] = []
    frame_starts: List[int] = []

    for idx, symbols in enumerate(frames):
        frame_num = idx + 1
        if not isinstance(symbols, (list, tuple)) or len(symbols) == 0:
            raise InvalidGameError(f"Frame {frame_num}: must be a non-empty list of rolls")

        frame_starts.append(len(flat_values))

        values: List[int] = []
        for roll_idx, symbol in enumerate(symbols):
            previous = values[roll_idx - 1] if roll_idx > 0 else None
            values.append(_parse_roll(symbol, previous))

        if frame_num < NUM_FRAMES:
            _validate_frame_1_to_9(frame_num, symbols, values)
        else:
            _validate_frame_10(symbols, values)

        flat_values.extend(values)

    return flat_values, frame_starts


def score_game(frames: Sequence[Sequence[str]]) -> List[int]:
    flat_values, frame_starts = _validate_and_flatten(frames)

    cumulative_scores: List[int] = []
    running_total = 0

    for frame_idx in range(NUM_FRAMES):
        start = frame_starts[frame_idx]
        first = flat_values[start]
        is_last_frame = frame_idx == NUM_FRAMES - 1

        if is_last_frame:
            frame_score = sum(flat_values[start:])
        elif first == STRIKE_PINS:
            frame_score = STRIKE_PINS + flat_values[start + 1] + flat_values[start + 2]
        elif first + flat_values[start + 1] == STRIKE_PINS:
            frame_score = STRIKE_PINS + flat_values[start + 2]
        else:
            frame_score = first + flat_values[start + 1]

        running_total += frame_score
        cumulative_scores.append(running_total)

    return cumulative_scores
