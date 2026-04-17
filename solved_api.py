# import requests
#
#
# def get_users(handles):
#
#     handles_str = ",".join(handles)
#
#     url = f"https://solved.ac/api/v3/user/lookup?handles={handles_str}"
#
#     headers = {
#         "User-Agent": "Mozilla/5.0"
#     }
#
#     r = requests.get(url, headers=headers, timeout=10)
#
#     if r.status_code != 200:
#         print("API ERROR:", r.status_code)
#         return []
#
#     data = r.json()
#     result = []
#
#     for user in data:
#
#         result.append({
#             "handle": user["handle"],
#             "solved": user["solvedCount"],
#             "tier": user["tier"],
#             "rating": user["rating"]
#         })
#
#     return result
#
# if __name__ == "__main__":
#     from students import students
#
#     users = get_users(students)
#
#     # print(students)
#
#
#     for i, user in enumerate(users, 1):
#         print(i, user)

'''
solced ac api가 막혀서 수동으로 students.json 파일을 다운로드 하고
이걸 기반으로 api 와 동일한 출력을 내는 get_user 함수를 만듬
'''

import json


TIER_TEXT_TO_NUM = {
    "Bronze V": 1,
    "Bronze IV": 2,
    "Bronze III": 3,
    "Bronze II": 4,
    "Bronze I": 5,
    "Silver V": 6,
    "Silver IV": 7,
    "Silver III": 8,
    "Silver II": 9,
    "Silver I": 10,
    "Gold V": 11,
    "Gold IV": 12,
    "Gold III": 13,
    "Gold II": 14,
    "Gold I": 15,
    "Platinum V": 16,
    "Platinum IV": 17,
    "Platinum III": 18,
    "Platinum II": 19,
    "Platinum I": 20,
    "Diamond V": 21,
    "Diamond IV": 22,
    "Diamond III": 23,
    "Diamond II": 24,
    "Diamond I": 25,
    "Ruby V": 26,
    "Ruby IV": 27,
    "Ruby III": 28,
    "Ruby II": 29,
    "Ruby I": 30,
    "Master": 31,
}


def tier_text_to_num(tier_text):
    if isinstance(tier_text, int):
        return tier_text
    return TIER_TEXT_TO_NUM.get(tier_text, 0)


def get_users(handles, path="students.json"):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    students = data.get("students", [])

    student_map = {
        s["username"]: s
        for s in students
    }

    result = []

    for h in handles:
        s = student_map.get(h)

        if not s:
            print(f"⚠️ 없음: {h}")
            continue

        result.append({
            "handle": s.get("username"),
            "solved": s.get("solved_count", 0),
            "tier": tier_text_to_num(s.get("tier")),
            "rating": s.get("rating", 0),
        })

    return result


if __name__ == "__main__":
    from students import students

    users = get_users(students)

    for i, user in enumerate(users, 1):
        print(i, user)