def tier_to_html(tier):

    tiers = [
        "Bronze V","Bronze IV","Bronze III","Bronze II","Bronze I",
        "Silver V","Silver IV","Silver III","Silver II","Silver I",
        "Gold V","Gold IV","Gold III","Gold II","Gold I",
        "Platinum V","Platinum IV","Platinum III","Platinum II","Platinum I",
        "Diamond V","Diamond IV","Diamond III","Diamond II","Diamond I",
        "Ruby V","Ruby IV","Ruby III","Ruby II","Ruby I"
    ]

    if tier == 0:
        return "Unrated"

    name = tiers[tier-1]

    if "Bronze" in name:
        color = "#ad5600"
    elif "Silver" in name:
        color = "#435f7a"
    elif "Gold" in name:
        color = "#ec9a00"
    elif "Platinum" in name:
        color = "#27e2a4"
    elif "Diamond" in name:
        color = "#00b4fc"
    else:
        color = "#ff0062"

    img = f"https://static.solved.ac/tier_small/{tier}.svg"

    return f'''
    <div style="display:flex;align-items:center;gap:6px">
        <img src="{img}" width="22">
        <span style="color:{color};font-weight:bold">{name}</span>
    </div>
    '''


def tier_to_text(tier):

    tiers = [
        "Bronze V","Bronze IV","Bronze III","Bronze II","Bronze I",
        "Silver V","Silver IV","Silver III","Silver II","Silver I",
        "Gold V","Gold IV","Gold III","Gold II","Gold I",
        "Platinum V","Platinum IV","Platinum III","Platinum II","Platinum I",
        "Diamond V","Diamond IV","Diamond III","Diamond II","Diamond I",
        "Ruby V","Ruby IV","Ruby III","Ruby II","Ruby I"
    ]

    if tier == 0:
        return "Unrated"

    return tiers[tier-1]