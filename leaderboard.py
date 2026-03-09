from students import students
from solved_api import get_users
from tiers import tier_to_html, tier_to_text
from history import update_today


def build_leaderboard():

    users = get_users(students)

    data = []

    for user in users:

        data.append({
            "name": user["handle"],
            "solved": user["solved"],
            "tier_html": tier_to_html(user["tier"]),
            "tier": tier_to_text(user["tier"])
        })

    data.sort(key=lambda x: x["solved"], reverse=True)

    for i, d in enumerate(data):
        d["rank"] = i + 1

    update_today(users)

    return data