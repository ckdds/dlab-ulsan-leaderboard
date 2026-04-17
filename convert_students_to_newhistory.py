import json
import os
from datetime import datetime, timezone, timedelta

'''
학생 데이터 수동 업데이트 하는 프로그램
solved_api_login_test.py 파일 실행 결과를 기존 시스템에 맞게 newhistory.json 파일로 만드는 과정
'''

STUDENTS_FILE = "students.json"
HISTORY_FILE = "history.json"

KST = timezone(timedelta(hours=9))


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def convert_students_to_history():
    students_data = load_json(STUDENTS_FILE)
    history_data = load_json(HISTORY_FILE)

    today = str(datetime.now(KST).date())

    students = students_data.get("students", [])

    # 🔥 rating 기준 정렬 → rank 계산
    students_sorted = sorted(
        students,
        key=lambda x: x.get("rating", 0),
        reverse=True
    )

    today_data = {}

    for rank, s in enumerate(students_sorted, 1):
        today_data[s["username"]] = {
            "solved": s.get("solved_count", 0),
            "rating": s.get("rating", 0),
            "rank": rank
        }

    history_data[today] = today_data

    save_json(HISTORY_FILE, history_data)

    print(f"✅ 변환 완료 → {HISTORY_FILE}")


if __name__ == "__main__":
    convert_students_to_history()