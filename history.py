import json
import os
from datetime import date, datetime, timezone, timedelta

FILE = "history.json"
KST = timezone(timedelta(hours=9))


def load_history():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_history(data):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def cleanup_history(history, keep_days=8):
    dates = sorted(history.keys())

    if len(dates) <= keep_days:
        return history

    old_dates = dates[:-keep_days]

    for d in old_dates:
        del history[d]

    return history


def get_solved_value(user_data):
    if isinstance(user_data, dict):
        return user_data.get("solved", 0)
    return user_data


def get_rating_value(user_data):
    if isinstance(user_data, dict):
        return user_data.get("rating", 0)
    return 0


def get_rank_value(user_data):
    if isinstance(user_data, dict):
        return user_data.get("rank", 0)
    return 0


def update_today(data):
    """
    반드시 leaderboard.py의 data 구조를 넘긴다고 가정:
    [
        {
            "name": "...",
            "solved": 123,
            "rating": 456,
            "rank": 1,
            ...
        },
        ...
    ]
    """
    history = load_history()
    today = str(datetime.now(KST).date())

    history[today] = {}

    for user in data:
        name = user["name"]
        history[today][name] = {
            "solved": user.get("solved", 0),
            "rating": user.get("rating", 0),
            "rank": user.get("rank", 0),
        }

    history = cleanup_history(history, keep_days=8)
    save_history(history)


def weekly_rising(data):
    history = load_history()

    today = datetime.now(KST).date()
    week = today - timedelta(days=7)
    week_str = str(week)

    if week_str not in history:
        return []

    week_data = history[week_str]
    rising = []

    for user in data:
        name = user["name"]
        now = user["solved"]
        before = get_solved_value(week_data.get(name, {}))

        rising.append({
            "name": name,
            "diff": now - before
        })

    rising.sort(key=lambda x: x["diff"], reverse=True)
    return rising[:3]


def today_hard_worker(data):
    history = load_history()

    today = datetime.now(KST).date()
    yesterday = today - timedelta(days=1)
    yesterday_str = str(yesterday)

    if yesterday_str not in history:
        return []

    yesterday_data = history[yesterday_str]
    rising = []

    for user in data:
        name = user["name"]
        now = user["solved"]
        before = get_solved_value(yesterday_data.get(name, {}))

        rising.append({
            "name": name,
            "diff": now - before
        })

    rising.sort(key=lambda x: x["diff"], reverse=True)
    return rising[:3]


def get_weekly_diff_map(data):
    """
    각 사용자별 solved / rating / rank 주간 변동 반환
    rank_diff:
      양수 = 순위 상승
      음수 = 순위 하락
    """
    history = load_history()

    today = datetime.now(KST).date()
    week = today - timedelta(days=7)
    week_str = str(week)

    if week_str not in history:
        return {
            user["name"]: {
                "solved_diff": 0,
                "rating_diff": 0,
                "rank_diff": 0,
            }
            for user in data
        }

    week_data = history[week_str]
    diff_map = {}

    for user in data:
        name = user["name"]

        past = week_data.get(name, {})
        past_solved = get_solved_value(past)
        past_rating = get_rating_value(past)
        past_rank = get_rank_value(past)

        now_solved = user.get("solved", 0)
        now_rating = user.get("rating", 0)
        now_rank = user.get("rank", 0)

        diff_map[name] = {
            "solved_diff": now_solved - past_solved,
            "rating_diff": now_rating - past_rating,
            "rank_diff": past_rank - now_rank if past_rank else 0,
        }

    return diff_map