from nicegui import ui, app, run
from leaderboard import build_leaderboard
from history import weekly_rising, today_hard_worker, get_weekly_diff_map
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

def rank_with_diff(rank, diff):
    if diff > 0:
        return (
            f'<div style="display:flex;justify-content:center;align-items:center;gap:8px;">'
            f'<span style="min-width:18px;text-align:right;">{rank}</span>'
            f'<span style="display:inline-block;min-width:32px;'
            f'padding:1px 5px;border-radius:999px;'
            f'background:#dcfce7;color:#16a34a;font-weight:700;font-size:12px;'
            f'text-align:center;">▲{diff}</span>'
            f'</div>'
        )
    elif diff < 0:
        return (
            f'<div style="display:flex;justify-content:center;align-items:center;gap:8px;">'
            f'<span style="min-width:18px;text-align:right;">{rank}</span>'
            f'<span style="display:inline-block;min-width:32px;'
            f'padding:1px 5px;border-radius:999px;'
            f'background:#fee2e2;color:#dc2626;font-weight:700;font-size:12px;'
            f'text-align:center;">▼{abs(diff)}</span>'
            f'</div>'
        )
    else:
        return (
            f'<div style="display:flex;justify-content:center;align-items:center;gap:8px;">'
            f'<span style="min-width:18px;text-align:right;">{rank}</span>'
            f'<span style="display:inline-block;min-width:32px;'
            f'padding:1px 5px;border-radius:999px;'
            f'background:#f3f4f6;color:#9ca3af;font-weight:600;font-size:12px;'
            f'text-align:center;">-</span>'
            f'</div>'
        )

def solved_with_diff(solved, diff):
    if diff > 0:
        diff_html = f'<span style="display:inline-block;width:34px;text-align:left;color:#15803d;font-weight:500;font-size:12px;opacity: 0.8;">+{diff}</span>'
    elif diff < 0:
        diff_html = f'<span style="display:inline-block;width:34px;text-align:left;color:#dc2626;font-weight:500;font-size:12px;opacity: 0.8;">{diff}</span>'
    else:
        diff_html = f'<span style="display:inline-block;width:34px;text-align:left;color:#d1d5db;font-size:12px;opacity: 0.8;">-</span>'

    return (
        f'<div style="display:inline-flex;align-items:center;justify-content:flex-start;'
        f'font-variant-numeric: tabular-nums;">'
        f'<span style="display:inline-block;width:36px;text-align:right;">{solved}</span>'
        f'<span style="display:inline-block;width:8px;"></span>'
        f'{diff_html}'
        f'</div>'
    )

def rating_with_diff(rating, diff):
    if diff > 0:
        diff_html = f'<span style="display:inline-block;width:40px;text-align:left;color:#2563eb;font-weight:500;font-size:12px;opacity: 0.8;">+{diff}</span>'
    elif diff < 0:
        diff_html = f'<span style="display:inline-block;width:40px;text-align:left;color:#dc2626;font-weight:500;font-size:12px;opacity: 0.8;">{diff}</span>'
    else:
        diff_html = f'<span style="display:inline-block;width:40px;text-align:left;color:#d1d5db;font-size:12px;opacity: 0.8;">-</span>'

    return (
        f'<div style="display:inline-flex;align-items:center;justify-content:flex-start;'
        f'font-variant-numeric: tabular-nums;">'
        f'<span style="display:inline-block;width:42px;text-align:right;">{rating}</span>'
        f'<span style="display:inline-block;width:8px;"></span>'
        f'{diff_html}'
        f'</div>'
    )


data = []

with ui.column().style("max-width:1300px;margin:auto;"):
    with ui.row().style("""
        width:100%;
        justify-content:center;
        align-items:center;
        gap:14px;
        margin:20px auto 20px auto;
    """):
        ui.image('logo.png').style("""
            width:160px;
            height:auto;
            display:block;
        """)
        ui.label('🏆 ').style("""
            font-size:26px;
            font-weight:bold;
            margin:0;
        """)
        ui.label('울산 알고리즘 리더보드').style("""
            font-size:32px;
            font-weight:bold;
            margin:0;
        """)

    # ui.label("🏆 DLAB 울산 알고리즘 리더보드").style("""
    #     font-size:40px;
    #     font-weight:bold;
    #     text-align:center;
    #     width:100%;
    #     margin-top:30px;
    #     margin-bottom:5px
    # """)

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

    ui.label("📊 전체 순위 (주간 변동)").style("font-size:24px;font-weight:bold")

    columns = [
        {"name": "rank", "label": "Rank", "field": "rank_display", "align": "center", "style": "width:140px"},
        {"name": "name", "label": "User", "field": "name", "align": "center"},
        {"name": "solved", "label": "Solved", "field": "solved_display", "align": "center", "style": "width:140px"},
        {"name": "rating", "label": "Rating", "field": "rating_display", "align": "center", "style": "width:150px"},
        {"name": "tier", "label": "Tier", "field": "tier", "align": "center"},
    ]

    table = ui.table(columns=columns, rows=data, row_key="name").style("""
        width:800px;
        margin:auto;
        font-size:18px;
        background: #ffffff;
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

    table.add_slot('body-cell-rank', r'''
    <q-td :props="props" style="text-align:center;">
        <div v-html="props.row.rank_display"></div>
    </q-td>
    ''')

    table.add_slot('body-cell-solved', r'''
    <q-td :props="props" style="text-align:center;">
        <div style="display:flex;justify-content:center;align-items:center;">
            <div v-html="props.row.solved_display"></div>
        </div>
    </q-td>
    ''')

    table.add_slot('body-cell-rating', r'''
    <q-td :props="props" style="text-align:center;">
        <div style="display:flex;justify-content:center;align-items:center;">
            <div v-html="props.row.rating_display"></div>
        </div>
    </q-td>
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

def load_data():
    try:
        data = build_leaderboard()
    except Exception as e:
        print("build_leaderboard error:", e)
        data = []

    try:
        diff_map = get_weekly_diff_map(data)
    except Exception as e:
        print("get_weekly_diff_map error:", e)
        diff_map = {}

    for row in data:
        d = diff_map.get(row["name"], {})
        rank_diff = d.get("rank_diff", 0)

        row["rank_diff"] = rank_diff
        row["solved_diff"] = d.get("solved_diff", 0)
        row["rating_diff"] = d.get("rating_diff", 0)

        row["rank_display"] = rank_with_diff(row["rank"], rank_diff)
        row["solved_display"] = solved_with_diff(
            row["solved"],
            d.get("solved_diff", 0)
        )
        row["rating_display"] = rating_with_diff(
            row["rating"],
            d.get("rating_diff", 0)
        )

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

    return data, weekly_data, today_data


async def load_and_render():
    data, weekly_data, today_data = await run.io_bound(load_data)

    table.rows = data
    table.update()

    render_top3(top3_container, data)
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