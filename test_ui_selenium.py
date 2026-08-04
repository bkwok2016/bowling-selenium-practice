"""
test_ui_selenium.py

Selenium tests for the bowling scorer web UI. Requires the Flask app
(app.py) to already be running at `base_url` before these tests execute.
See README.md for exactly how to run this locally and in CI.
"""

import pytest

from pages.bowling_page import BowlingPage
from bowling_game import score_game


EXAMPLE_GAME = [
    ["8", "/"], ["5", "4"], ["9", "0"], ["X"], ["X"],
    ["5", "/"], ["5", "3"], ["6", "3"], ["9", "/"], ["9", "/", "X"],
]
PERFECT_GAME = [["X"]] * 9 + [["X", "X", "X"]]
ALL_OPEN_GAME = [["4", "3"]] * 10


# ---------------------------------------------------------------------------
# Valid games -> correct score displayed
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "frames",
    [EXAMPLE_GAME, PERFECT_GAME, ALL_OPEN_GAME],
    ids=["example_game", "perfect_game", "all_open_frames"],
)
def test_valid_game_displays_correct_total(driver, base_url, frames):
    page = BowlingPage(driver, base_url)
    page.load()
    page.enter_frames(frames)
    page.submit()

    expected_total = score_game(frames)[-1]
    assert page.get_final_score() == str(expected_total)


def test_valid_game_displays_correct_cumulative_scores(driver, base_url):
    page = BowlingPage(driver, base_url)
    page.load()
    page.enter_frames(EXAMPLE_GAME)
    page.submit()

    expected_scores = score_game(EXAMPLE_GAME)
    for i, expected in enumerate(expected_scores):
        assert page.get_cumulative_score(i) == str(expected)


# ---------------------------------------------------------------------------
# Invalid input -> error message displayed, no results shown
# ---------------------------------------------------------------------------

def test_invalid_symbol_shows_error_message(driver, base_url):
    page = BowlingPage(driver, base_url)
    page.load()
    frames = [["Z", "3"]] + [["0", "0"]] * 9
    page.enter_frames(frames)
    page.submit()

    error = page.get_error_message()
    assert error is not None
    assert "Invalid roll symbol" in error


def test_spare_as_first_roll_shows_error_message(driver, base_url):
    page = BowlingPage(driver, base_url)
    page.load()
    frames = [["/", "5"]] + [["3", "4"]] * 9
    page.enter_frames(frames)
    page.submit()

    error = page.get_error_message()
    assert error is not None
    assert "spare" in error.lower()


def test_empty_frame_shows_error_message(driver, base_url):
    page = BowlingPage(driver, base_url)
    page.load()

    page.enter_frame(0, "")  # leave frame 1 blank
    for i in range(1, 10):
        page.enter_frame(i, "3,4")
    page.submit()

    error = page.get_error_message()
    assert error is not None
    assert "empty" in error.lower()


def test_tenth_frame_missing_bonus_roll_shows_error(driver, base_url):
    page = BowlingPage(driver, base_url)
    page.load()
    frames = [["3", "4"]] * 9 + [["X"]]  # strike with no bonus rolls
    page.enter_frames(frames)
    page.submit()

    error = page.get_error_message()
    assert error is not None
    assert "bonus" in error.lower()


# ---------------------------------------------------------------------------
# Re-submission behavior
# ---------------------------------------------------------------------------

def test_resubmitting_a_corrected_game_clears_previous_error(driver, base_url):
    page = BowlingPage(driver, base_url)
    page.load()

    # First submit something invalid
    invalid_frames = [["Z", "3"]] + [["0", "0"]] * 9
    page.enter_frames(invalid_frames)
    page.submit()
    assert page.get_error_message() is not None

    # Now correct frame 1 and resubmit the rest of a valid game
    page.enter_frames(ALL_OPEN_GAME)
    page.submit()

    assert page.get_error_message() is None
    assert page.get_final_score() == str(score_game(ALL_OPEN_GAME)[-1])
