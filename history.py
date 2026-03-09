import json
import os
from datetime import date

FILE = "history.json"


def load_history():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        return json.load(f)


def save_history(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=2)


def update_today(data):
    history = load_history()

    today = str(date.today())

    if today not in history:
        history[today] = {}

    for user in data:
        history[today][user["handle"]] = user["solved"]

    save_history(history)


def weekly_rising(data):
    history = load_history()

    if len(history) < 2:
        return []

    dates = sorted(history.keys())

    today = dates[-1]
    week = dates[0] if len(dates) < 7 else dates[-7]

    rising = []

    for user in data:

        name = user["name"]
        now = user["solved"]

        before = history.get(week, {}).get(name, now)

        diff = now - before

        rising.append({
            "name": name,
            "diff": diff
        })

    rising.sort(key=lambda x: x["diff"], reverse=True)

    return rising[:3]


def today_hard_worker(data):

    history = load_history()

    today = str(date.today())

    if today not in history:
        return []

    today_data = history[today]

    rising = []

    for user in data:

        name = user["name"]
        now = user["solved"]

        before = today_data.get(name, now)

        diff = now - before

        rising.append({
            "name": name,
            "diff": diff
        })

    rising.sort(key=lambda x: x["diff"], reverse=True)

    return rising[:3]