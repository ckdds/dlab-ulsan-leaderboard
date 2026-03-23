from nicegui import ui, app
from leaderboard import build_leaderboard
from history import weekly_rising, today_hard_worker
from datetime import datetime, timezone, timedelta
from fastapi.responses import FileResponse, PlainTextResponse
import os

KST = timezone(timedelta(hours=9))
HISTORY_FILE = "history.json"


@app.get('/download/history')
def download_history():
    if not os.path.exists(HISTORY_FILE):
        return PlainTextResponse('history.json 파일이 없습니다.', status_code=404)

    return FileResponse(
        path=HISTORY_FILE,
        filename='history.json',
        media_type='application/json'
    )

def render_top3(container, data):
    container.clear()

    if not data:
        with container:
            ui.label("TOP 3 데이터를 불러오지 못했습니다.").style("color:gray")
        return

    with container:
        if len(data) < 3:
            top3 = data
        else:
            top3 = [data[1], data[0], data[2]]
        
        medals = ["🥈", "🥇", "🥉"]

        for i, user in enumerate(top3):
            medal = medals[i]

            width = "300px" if i == 1 else "220px"
            height = "250px" if i == 1 else "230px"
            gap = "12px" if i == 1 else "8px"
            bg = "background:#fff7cc;" if i == 1 else ""

            with ui.card().style(f"""
                width:{width};
                height:{height};
                display:flex;
                flex-direction:column;
                align-items:center;
                justify-content:center;
                gap:{gap};
                box-shadow:0 4px 10px rgba(0,0,0,0.1);
                border-radius:12px;
                {bg}
            """):
                ui.label(medal).style("font-size:36px;margin-bottom:3px")
                ui.label(user["name"]).style("font-size:20px;font-weight:bold")

                with ui.row().style("align-items:end;justify-content:center;gap:6px"):
                    ui.label("Rating").style(
                        "font-size:17px;color:gray;margin-bottom:6px"
                    )
                    ui.label(str(user["rating"])).style(
                        "font-size:36px;font-weight:800;color:#2563eb"
                    )

                ui.html(user["tier_html"])


def render_rising(container, rising_data, title_type="solved"):
    container.clear()

    if not rising_data:
        with container:
            ui.label("표시할 데이터가 없습니다.").style("color:gray")
        return

    with container:
        for i, r in enumerate(rising_data):
            with ui.card().style(
                "width:220px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.1)"
            ):
                ui.label(f"{i+1}. {r['name']}").style("font-weight:bold")
                ui.label(f"+{r['diff']} {title_type}").style(
                    "color:green;font-weight:bold"
                )


data = []
with ui.column().style("max-width:1300px;margin:auto"):
    ui.label("🏆 DLAB 울산 알고리즘 리더보드").style("""
        font-size:40px;
        font-weight:bold;
        text-align:center;
        width:100%;
        margin-top:30px;
        margin-bottom:5px
    """)

    ui.separator()

    with ui.row().style("width:100%;justify-content:flex-end"):
        ui.link(
            '📥 history.json 다운로드',
            '/download/history'
        ).props('target=_blank').style(
            "color:#2563eb;font-weight:bold;text-decoration:none"
        )

        last_update_label = ui.label(
            f"Last update : {datetime.now(KST).strftime('%H:%M:%S')}"
        ).style("color:gray;margin-bottom:10px")

    ui.label("🥇 TOP 3").style("font-size:24px;font-weight:bold")
    top3_container = ui.row().style("""
        gap:30px;
        justify-content:center;
        align-items:flex-end;
        margin-bottom:30px;
    """)
    render_top3(top3_container, data)

    ui.separator()

    ui.label("📊 전체 순위").style("font-size:24px;font-weight:bold")

    columns = [
        {"name": "rank", "label": "Rank", "field": "rank", "align": "center"},
        {"name": "name", "label": "User", "field": "name", "align": "center"},
        {"name": "solved", "label": "Solved", "field": "solved", "align": "center"},
        {"name": "rating", "label": "Rating", "field": "rating", "align": "center"},
        {"name": "tier", "label": "Tier", "field": "tier", "align": "center"},
    ]

    table = ui.table(columns=columns, rows=data, row_key="name").style("""
        width:800px;
        margin:auto;
        font-size:18px;
    """)
    table.props('dense')

    table.add_slot('header', r'''
    <tr>
    <th style="font-size:18px;text-align:center">순위</th>
    <th style="font-size:18px;text-align:center">아이디</th>
    <th style="font-size:18px;text-align:center">문제해결</th>
    <th style="font-size:18px;text-align:center">Rating</th>
    <th style="font-size:18px;text-align:center">티어</th>
    </tr>
    ''')

    ui.separator().style("margin-top:30px;margin-bottom:0px")

    ui.label("🔥 이번 주 문제 해결 TOP 3").style("font-size:24px;font-weight:bold")
    weekly_container = ui.row().style(
        "gap:40px;justify-content:center;margin-bottom:30px"
    )

    ui.separator()

    ui.label("🚀 오늘 문제 해결 TOP 3").style("font-size:24px;font-weight:bold")
    today_container = ui.row().style(
        "gap:40px;justify-content:center;margin-bottom:30px"
    )


def load_and_render():
    try:
        data = build_leaderboard()
    except Exception as e:
        print("build_leaderboard error:", e)
        data = []

    table.rows = data
    table.update()

    render_top3(top3_container, data)

    try:
        weekly_data = weekly_rising(data)
    except Exception as e:
        print("weekly_rising error:", e)
        weekly_data = []

    try:
        today_data = today_hard_worker(data)
    except Exception as e:
        print("today_hard_worker error:", e)
        today_data = []

    render_rising(weekly_container, weekly_data)
    render_rising(today_container, today_data)

    last_update_label.set_text(
        f"Last update : {datetime.now(KST).strftime('%H:%M:%S')}"
    )


ui.timer(60, load_and_render, immediate=True)

port = int(os.environ.get("PORT", 8080))

ui.run(
    host="0.0.0.0",
    port=port,
    title="DLAB Algo Rank",
    favicon='static/favicon.png'
)