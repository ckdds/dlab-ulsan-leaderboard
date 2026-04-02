import requests


def get_users(handles):

    handles_str = ",".join(handles)

    url = f"https://solved.ac/api/v3/user/lookup?handles={handles_str}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers, timeout=5)

    if r.status_code != 200:
        print("API ERROR:", r.status_code)
        return []

    data = r.json()
    result = []

    for user in data:

        result.append({
            "handle": user["handle"],
            "solved": user["solvedCount"],
            "tier": user["tier"],
            "rating": user["rating"]
        })

    return result

if __name__ == "__main__":
    from students import students

    users = get_users(students)

    print(students)


    # for i, user in enumerate(users, 1):
    #     print(i, user)