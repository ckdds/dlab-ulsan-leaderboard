# from students import students
# from solved_api import get_users
# from tiers import tier_to_html, tier_to_text
# from history import update_today
#
#
# def build_leaderboard():
#     users = get_users(students)
#
#     data = []
#
#     for user in users:
#         data.append({
#             "name": user["handle"],
#             "solved": user["solved"],
#             "tier_html": tier_to_html(user["tier"]),
#             "tier": tier_to_text(user["tier"]),
#             "rating": user["rating"]
#         })
#
#     data.sort(key=lambda x: x["rating"], reverse=True)
#
#     for i, d in enumerate(data):
#         d["rank"] = i + 1
#
#     update_today(data)
#
#     return data
#
#
# if __name__ == "__main__":
#     leaderboard = build_leaderboard()
#
#     for row in leaderboard:
#         print(row)


import json
from tiers import tier_to_html, tier_to_text


def build_leaderboard():
    try:
        with open("history.json", "r", encoding="utf-8") as f:
            history = json.load(f)
    except Exception as e:
        print(f"❌ history.json 읽기 실패: {e}")
        return []

    if not history:
        print("⚠️ history 데이터 없음")
        return []

    latest_date = sorted(history.keys())[-1]
    # print(f"📅 최신 날짜: {latest_date}")

    latest_data = history[latest_date]

    result = []

    for name, info in latest_data.items():
        rating = info.get("rating", 0)

        # rating만 가지고는 정확한 tier 복원이 안 되므로
        # history에 tier가 없으면 0 처리
        tier = info.get("tier", 0)

        result.append({
            "name": name,
            "solved": info.get("solved", 0),
            "rating": rating,
            "rank": info.get("rank", 0),
            "tier_html": tier_to_html(tier),
            "tier": tier_to_text(tier),
        })

    result.sort(key=lambda x: x["rank"])
    return result


if __name__ == "__main__":
    leaderboard = build_leaderboard()

    for row in leaderboard:
        print(row)