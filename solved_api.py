import requests


def get_users(handles):

    handles_str = ",".join(handles)

    url = f"https://solved.ac/api/v3/user/lookup?handles={handles_str}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)

    if r.status_code != 200:
        print("API ERROR:", r.status_code)
        return []

    data = r.json()

    result = []

    for user in data:

        result.append({
            "handle": user["handle"],
            "solved": user["solvedCount"],
            "tier": user["tier"]
        })

    return result