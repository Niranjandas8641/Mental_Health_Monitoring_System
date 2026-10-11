import json
from datetime import datetime, timedelta
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from textblob import TextBlob


app = Flask(__name__)

DATA_FILE = Path(__file__).with_name("mental_health_data.json")


class MentalHealthMonitor:

    def __init__(self):
        self.data_file = DATA_FILE
        self.data = self.load_data()

    def load_data(self):
        if not self.data_file.exists():
            return {"entries": []}

        try:
            with open(self.data_file, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, dict) and isinstance(
                data.get("entries"), list
            ):
                return data

        except (json.JSONDecodeError, OSError):
            app.logger.exception("Could not load mood data.")

        return {"entries": []}

    def save_data(self):
        with open(self.data_file, "w", encoding="utf-8") as file:
            json.dump(
                self.data,
                file,
                indent=4,
                ensure_ascii=False
            )

    def analyze_sentiment(self, notes):
        if not notes.strip():
            return "neutral"

        polarity = TextBlob(notes).sentiment.polarity

        if polarity > 0.1:
            return "positive"
        elif polarity < -0.1:
            return "negative"

        return "neutral"

    def log_mood(self, mood_score, notes=""):
        if (
            isinstance(mood_score, bool)
            or not isinstance(mood_score, int)
            or not 1 <= mood_score <= 5
        ):
            raise ValueError("Mood must be an integer from 1 to 5.")

        if not isinstance(notes, str):
            raise ValueError("Notes must be text.")

        notes = notes.strip()

        if len(notes) > 500:
            raise ValueError("Notes must not exceed 500 characters.")

        entry = {
            "timestamp": datetime.now().astimezone().isoformat(
                timespec="seconds"
            ),
            "mood_score": mood_score,
            "notes": notes,
            "sentiment": self.analyze_sentiment(notes)
        }

        self.data["entries"].append(entry)
        self.save_data()

        return entry

    def get_summary(self):
        cutoff = datetime.now().astimezone() - timedelta(days=30)
        recent_entries = []

        for entry in self.data["entries"]:
            try:
                timestamp = datetime.fromisoformat(entry["timestamp"])

                if timestamp.tzinfo is None:
                    timestamp = timestamp.astimezone()

                if timestamp >= cutoff:
                    recent_entries.append(entry)

            except (ValueError, KeyError, TypeError):
                continue

        scores = [
            entry["mood_score"]
            for entry in recent_entries
            if type(entry.get("mood_score")) is int
            and 1 <= entry["mood_score"] <= 5
        ]

        average = round(sum(scores) / len(scores), 2) if scores else 0

        return {
            "total_entries": len(self.data["entries"]),
            "total_entries_30_days": len(recent_entries),
            "avg_mood_30_days": average,
            "last_entry": (
                self.data["entries"][-1].get("timestamp")
                if self.data["entries"]
                else None
            ),
            "recent_entries": recent_entries
        }


monitor = MentalHealthMonitor()


def get_weekly_analysis():
    """Calculate mood statistics for the last seven local calendar days."""

    today = datetime.now().astimezone().date()
    first_day = today - timedelta(days=6)

    daily_moods = {
        first_day + timedelta(days=i): []
        for i in range(7)
    }

    entries = monitor.data.get("entries", [])

    for entry in entries:
        if not isinstance(entry, dict):
            continue

        mood = entry.get("mood_score", entry.get("mood"))

        timestamp = (
            entry.get("timestamp")
            or entry.get("date")
            or entry.get("created_at")
        )

        if mood is None or timestamp is None:
            continue

        try:
            # Validate mood without silently accepting decimals.
            if isinstance(mood, bool):
                continue

            mood_number = float(mood)

            if not mood_number.is_integer():
                continue

            mood_number = int(mood_number)

            if not 1 <= mood_number <= 5:
                continue

            # Parse timestamp or date.
            if isinstance(timestamp, (int, float)):
                entry_date = datetime.fromtimestamp(
                    timestamp
                ).astimezone().date()
            else:
                date_text = str(timestamp).strip()

                try:
                    parsed = datetime.fromisoformat(
                        date_text.replace("Z", "+00:00")
                    )

                    if parsed.tzinfo is not None:
                        parsed = parsed.astimezone()

                    entry_date = parsed.date()

                except ValueError:
                    entry_date = datetime.strptime(
                        date_text[:10], "%Y-%m-%d"
                    ).date()

            if first_day <= entry_date <= today:
                daily_moods[entry_date].append(mood_number)

        except (ValueError, TypeError, OverflowError, OSError):
            continue

    labels = []
    daily_averages = []
    daily_entry_counts = []

    for day, moods in daily_moods.items():
        labels.append(day.strftime("%a"))

        daily_averages.append(
            round(sum(moods) / len(moods), 2) if moods else None
        )

        daily_entry_counts.append(len(moods))

    all_moods = [
        mood
        for moods in daily_moods.values()
        for mood in moods
    ]

    weekly_average = (
        round(sum(all_moods) / len(all_moods), 2)
        if all_moods
        else None
    )

    earlier_moods = [
        mood
        for day, moods in daily_moods.items()
        if day <= today - timedelta(days=3)
        for mood in moods
    ]

    later_moods = [
        mood
        for day, moods in daily_moods.items()
        if day > today - timedelta(days=3)
        for mood in moods
    ]

    if earlier_moods and later_moods:
        difference = (
            sum(later_moods) / len(later_moods)
            - sum(earlier_moods) / len(earlier_moods)
        )

        if difference >= 0.5:
            trend = "Improving"
        elif difference <= -0.5:
            trend = "Declining"
        else:
            trend = "Relatively stable"
    else:
        trend = "Not enough data"

    return {
        "period": {
            "start": first_day.isoformat(),
            "end": today.isoformat()
        },
        "weekly_average": weekly_average,
        "total_entries": len(all_moods),
        "trend": trend,
        "labels": labels,
        "daily_averages": daily_averages,
        "daily_entry_counts": daily_entry_counts
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/log_mood", methods=["POST"])
def log_mood():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send valid JSON data."
        }), 400

    mood = data.get("mood")
    note = data.get("note", "")

    if type(mood) is not int or not 1 <= mood <= 5:
        return jsonify({
            "error": "Mood must be a whole number from 1 to 5."
        }), 400

    if not isinstance(note, str):
        return jsonify({
            "error": "Note must be text."
        }), 400

    if len(note.strip()) > 500:
        return jsonify({
            "error": "Notes must not exceed 500 characters."
        }), 400

    try:
        entry = monitor.log_mood(mood, note)

        return jsonify({
            "message": "Mood saved successfully.",
            "record": entry,
            "analysis": {
                "sentiment": entry["sentiment"]
            }
        }), 201

    except (ValueError, OSError):
        app.logger.exception("Could not save mood entry.")
        return jsonify({
            "error": "Unable to save the mood entry."
        }), 500


@app.route("/api/summary", methods=["GET"])
def summary():
    try:
        return jsonify(monitor.get_summary())
    except Exception:
        app.logger.exception("Could not load mood summary.")
        return jsonify({
            "error": "Unable to load mood summary."
        }), 500


@app.route("/api/weekly-analysis", methods=["GET"])
def weekly_analysis():
    try:
        return jsonify(get_weekly_analysis())
    except Exception:
        app.logger.exception("Could not calculate weekly analysis.")
        return jsonify({
            "error": "Unable to calculate weekly mood analysis."
        }), 500


if __name__ == "__main__":
    app.run(debug=True)