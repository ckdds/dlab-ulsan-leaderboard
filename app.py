from nicegui import ui
from leaderboard import build_leaderboard
from history import weekly_rising, today_hard_worker
from datetime import datetime, timezone, timedelta
import os

# 리더보드 데이터 생성
data = build_leaderboard()
KST = timezone(timedelta(hours=9))

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
        last_update_label = ui.label(
            f"Last update : {datetime.now(KST).strftime('%H:%M:%S')}"
        ).style("color:gray;margin-bottom:10px")

    # TOP3

    ui.label("🥇 TOP 3").style(
        "font-size:24px;font-weight:bold"
    )

    top3_container = ui.row().style("""
        gap:30px;
        justify-content:center;
        align-items:flex-end;
        margin-bottom:30px;
    """)

    with top3_container:

        top3 = [data[1], data[0], data[2]]

        for i, user in enumerate(top3):

            medals = ["🥈", "🥇", "🥉"]
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

                ui.label(medal).style(
                    "font-size:36px;margin-bottom:3px"
                )

                ui.label(user["name"]).style(
                    "font-size:20px;font-weight:bold"
                )

                with ui.row().style("align-items:end;justify-content:center;gap:6px"):

                    ui.label(user["solved"]).style(
                        "font-size:36px;font-weight:800;color:#2563eb"
                    )

                    ui.label("solved").style(
                        "font-size:17px;color:gray;margin-bottom:6px"
                    )

                ui.html(user["tier_html"])


    # Leaderboard

    ui.separator()

    ui.label("📊 전체 순위").style(
        "font-size:24px;font-weight:bold"
    )

    columns = [
        {"name": "rank", "label": "Rank", "field": "rank", "align": "center"},
        {"name": "name", "label": "User", "field": "name", "align": "center"},
        {"name": "solved", "label": "Solved", "field": "solved", "align": "center"},
        {"name": "tier", "label": "Tier", "field": "tier", "align": "center"},
    ]

    table = ui.table(
        columns=columns,
        rows=data,
        row_key="name"
    ).style("""
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
    <th style="font-size:18px;text-align:center">티어</th>
    </tr>
    ''')

    # Weekly Rising

    ui.separator().style("margin-top:30px;margin-bottom:0px")

    ui.label("🔥 이번 주 문제 해결 TOP 3").style(
        "font-size:24px;font-weight:bold"
    )

    weekly_container = ui.row().style(
        "gap:40px;justify-content:center;margin-bottom:30px"
    )

    with weekly_container:

        rising = weekly_rising(data)

        for i, r in enumerate(rising):

            with ui.card().style(
                "width:220px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.1)"
            ):

                ui.label(f"{i+1}. {r['name']}").style(
                    "font-weight:bold"
                )

                ui.label(f"+{r['diff']} solved").style(
                    "color:green;font-weight:bold"
                )

    # Today Hard Worker

    ui.separator()

    ui.label("🚀 오늘 문제 해결 TOP 3").style(
        "font-size:24px;font-weight:bold"
    )

    today_container = ui.row().style(
        "gap:40px;justify-content:center;margin-bottom:30px"
    )

    with today_container:

        today = today_hard_worker(data)

        for i, r in enumerate(today):

            with ui.card().style(
                "width:220px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.1)"
            ):

                ui.label(f"{i+1}. {r['name']}").style(
                    "font-weight:bold"
                )

                ui.label(f"+{r['diff']} solved").style(
                    "color:green;font-weight:bold"
                )


# =========================
# refresh 함수
# =========================

def refresh():

    new_data = build_leaderboard()

    # 테이블 업데이트
    table.rows = new_data
    table.update()

    # TOP3 업데이트
    top3_container.clear()

    with top3_container:

        top3 = [new_data[1], new_data[0], new_data[2]]

        for i, user in enumerate(top3):
            medals = ["🥈", "🥇", "🥉"]
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

                ui.label(medal).style("font-size:36px")

                ui.label(user["name"]).style(
                    "font-size:20px;font-weight:bold"
                )

                with ui.row().style("align-items:end;justify-content:center;gap:6px"):

                    ui.label(user["solved"]).style(
                        "font-size:36px;font-weight:800;color:#2563eb"
                    )

                    ui.label("solved").style(
                        "font-size:17px;color:gray;margin-bottom:6px"
                    )

                ui.html(user["tier_html"])

    # Weekly Rising 업데이트
    weekly_container.clear()

    rising = weekly_rising(new_data)
    with weekly_container:
        for i, r in enumerate(rising):
            with ui.card().style(
                "width:220px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.1)"
            ):

                ui.label(f"{i+1}. {r['name']}").style("font-weight:bold")

                ui.label(f"+{r['diff']} solved").style(
                    "color:green;font-weight:bold"
                )

    # Today Hard Worker 업데이트
    today_container.clear()

    today = today_hard_worker(new_data)

    with today_container:
        for i, r in enumerate(today):
            with ui.card().style(
                "width:220px;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.1)"
            ):

                ui.label(f"{i+1}. {r['name']}").style("font-weight:bold")

                ui.label(f"+{r['diff']} solved").style(
                    "color:green;font-weight:bold"
                )

    # 업데이트 시간
    last_update_label.set_text(
        f"Last update : {datetime.now(KST).strftime('%H:%M:%S')}"
    )


ui.timer(60, refresh, immediate=True)

port = int(os.environ.get("PORT", 8080))

ui.run(
    host="0.0.0.0",
    port=port,
    title="DLAB Algo Rank",
    favicon="https://cdn-icons-png.flaticon.com/512/2583/2583344.png"
)