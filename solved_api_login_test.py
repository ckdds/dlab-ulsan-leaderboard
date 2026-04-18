import re
import json
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


'''
실행 방법
그냥 solved ac에 접속해서 학생 현재 데이터 가져오기 실패 403 에러

왜 아래와 같은 방법을 사용하나?
일반적인 방법:
requests ❌
selenium ❌
playwright 새 브라우저 ❌
👉 전부 Cloudflare에 막힘

그래서 사용한 방법
크롬 디버그 모드 + CDP 연결 = “사람 브라우저를 그대로 사용하기 위해서” 

지금 방식 (CDP)
이미 켜져 있는 크롬에 붙음
로그인 / 쿠키 / Cloudflare 통과 상태 그대로 사용
👉 사람처럼 보임

1. 크롬실행 (Ctrl + R)
chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrome_debug

2. 그 크롬에서 solved.ac 열기

3. 이 코드 실행
'''


students = [
    'happy_rabbit',
    'rem_maji_tenshi',
    'jason0112',
    'wsy8789',
    'min_tainumone',
    'superspider1158',
    'melodykim',
    'tangblyty',
    'junseong_kim',
    'bori_12',
    'speedgldsos',
    'bshbsh0424',
    'firetmxk_123',
    'yejun1223',
    'yonusalis',
    'pmcozxcv',
    'minjungi_10',
    'chl_dnjs',
    'doyi2010'
]


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_profile_text(page_text: str, username: str) -> dict:
    data = {
        "username": username,
        "tier": None,
        "rating": None,
        "next_tier": None,
        "to_next_tier": None,
        "solved_count": None,
        "rival_count": None,
        "global_rank": None,
        "top_percent": None,
        "class_level": None,
        "class_score": None,
    }

    text = clean_text(page_text)

    # 예: Silver I 734 Gold V 승급까지 -66
    m = re.search(
        r"\b(Bronze|Silver|Gold|Platinum|Diamond|Ruby)\s+([IVX]+)\s+(\d+)"
        r"(?:\s+(Bronze|Silver|Gold|Platinum|Diamond|Ruby)\s+([IVX]+)\s+승급까지\s*([−-]?\d+))?",
        text
    )
    if m:
        data["tier"] = f"{m.group(1)} {m.group(2)}"
        data["rating"] = int(m.group(3))
        if m.group(4) and m.group(5):
            data["next_tier"] = f"{m.group(4)} {m.group(5)}"
        if m.group(6):
            data["to_next_tier"] = int(m.group(6).replace("−", "-"))

    # 예: 156 문제 해결 1명의 라이벌
    m = re.search(r"(\d+)\s*문제 해결\s*(\d+)\s*명의 라이벌", text)
    if m:
        data["solved_count"] = int(m.group(1))
        data["rival_count"] = int(m.group(2))

    # 예: #64,636 전체 ↑34.40%
    m = re.search(r"#([\d,]+)\s*전체\s*[↑↓]?([\d.]+%)", text)
    if m:
        data["global_rank"] = int(m.group(1).replace(",", ""))
        data["top_percent"] = m.group(2)

    # 예: CLASS 2 + 50
    m = re.search(r"CLASS\s+(\d+)\s*\+\s*(\d+)", text)
    if m:
        data["class_level"] = int(m.group(1))
        data["class_score"] = int(m.group(2))

    return data


def create_driver():
    options = Options()
    options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(30)
    return driver


def wait_until_loaded(driver, username: str, timeout: int = 15):
    wait = WebDriverWait(driver, timeout)

    # body가 뜰 때까지
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # 페이지 텍스트에 username이 보일 때까지 조금 기다림
    end_time = time.time() + timeout
    while time.time() < end_time:
        text = driver.find_element(By.TAG_NAME, "body").text
        if username in text:
            return
        time.sleep(0.5)

    # username이 꼭 안 보여도 body는 읽을 수 있으니 그냥 진행
    return


def fetch_profile(driver, username: str) -> dict:
    url = f"https://solved.ac/profile/{username}"
    print(f"접속: {url}")
    driver.get(url)
    wait_until_loaded(driver, username)

    body_text = driver.find_element(By.TAG_NAME, "body").text
    data = parse_profile_text(body_text, username)
    data["url"] = url
    return data


def collect_profiles(student_list):
    driver = create_driver()
    results = []

    try:
        for i, username in enumerate(student_list, 1):
            print(f"[{i}/{len(student_list)}] 수집 중: {username}")
            try:
                profile = fetch_profile(driver, username)

                if profile["rating"] is None and profile["solved_count"] is None:
                    print(f"⚠️ 파싱 실패: {username}")
                else:
                    print(
                        f"✅ {username} / solved={profile['solved_count']} / "
                        f"rating={profile['rating']} / tier={profile['tier']}"
                    )
                    results.append(profile)

            except Exception as e:
                print(f"❌ 에러: {username} / {e}")

            time.sleep(1.5)

    finally:
        # 붙어 있던 크롬 자체를 끄고 싶지 않으면 quit 안 하는 것도 가능
        try:
            driver.quit()
        except Exception:
            pass

    return results


def save_json(data, filename="students.json"):
    output = {
        # "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": datetime.now().strftime("%Y-%m-%d"), # 시간 데이터 필요 없어서 삭제
        "count": len(data),
        "students": data,
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n저장 완료: {filename}")


if __name__ == "__main__":
    result = collect_profiles(students)
    save_json(result, "students.json")