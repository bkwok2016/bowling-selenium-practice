"""
app.py

A minimal Flask web UI for the bowling game scorer, built specifically to
give Selenium something real to click through: a form, a submit button,
a results section, and a validation error message.

Run with:
    python app.py
Then open http://localhost:5000 in a browser.
"""

from flask import Flask, render_template, request

from bowling_game import score_game, InvalidGameError

app = Flask(__name__)


def parse_frames_from_form(form) -> list:
    """
    Reads frame-0 .. frame-9 from the submitted form and turns each into
    a list of roll symbols, e.g. "8,/" -> ["8", "/"].
    """
    frames = []
    for i in range(10):
        raw = form.get(f"frame-{i}", "").strip()
        if raw == "":
            raise InvalidGameError(f"Frame {i + 1} is empty")
        rolls = [r.strip() for r in raw.split(",") if r.strip() != ""]
        if not rolls:
            raise InvalidGameError(f"Frame {i + 1} is empty")
        frames.append(rolls)
    return frames


@app.route("/", methods=["GET"])
def index():
    return render_template(
        "index.html", scores=None, total=None, error=None, values=[""] * 10
    )


@app.route("/score", methods=["POST"])
def calculate_score():
    raw_values = [request.form.get(f"frame-{i}", "") for i in range(10)]
    try:
        frames = parse_frames_from_form(request.form)
        scores = score_game(frames)
        total = scores[-1]
        return render_template(
            "index.html", scores=scores, total=total, error=None, values=raw_values
        )
    except InvalidGameError as e:
        return render_template(
            "index.html", scores=None, total=None, error=str(e), values=raw_values
        )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
