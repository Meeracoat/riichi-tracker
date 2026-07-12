import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

from storage import load_matches


st.title("📊 Dashboard")


# -------------------------
# HTML Card
# -------------------------

def stat_card(title, value, icon):

    html = f"""
    <div style="
        background:#1c1f26;
        border-radius:15px;
        padding:20px;
        text-align:center;
        height:120px;
        box-shadow:0 4px 10px rgba(0,0,0,0.25);
        margin-bottom:15px;
        color:white;
        font-family:sans-serif;
    ">

        <div style="
            font-size:25px;
        ">
            {icon}
        </div>


        <div style="
            font-size:32px;
            font-weight:bold;
        ">
            {value}
        </div>


        <div style="
            font-size:14px;
            opacity:0.8;
        ">
            {title}
        </div>


    </div>
    """

    components.html(
        html,
        height=170
    )


# -------------------------
# Load username
# -------------------------
username = st.session_state.get(
    "username",
    ""
)


if username == "":

    st.info(
        "Enter your username in the sidebar."
    )

    st.stop()


# -------------------------
# Load matches
# -------------------------

matches = load_matches(username)


if not matches:

    st.info(
        "No games imported yet."
    )

    st.stop()


df = pd.DataFrame(matches)


# -------------------------
# Compatibility with old data
# -------------------------

if "Players" not in df.columns:

    df["Players"] = 3


# -------------------------
# Format filter
# -------------------------

st.subheader(
    "Game Format"
)


format_filter = st.selectbox(
    "View",
    [
        "All Games",
        "3 Player",
        "4 Player"
    ]
)


filtered = df.copy()


if format_filter == "3 Player":

    filtered = filtered[
        filtered["Players"] == 3
    ]


elif format_filter == "4 Player":

    filtered = filtered[
        filtered["Players"] == 4
    ]


if filtered.empty:

    st.info(
        "No games found."
    )

    st.stop()


# -------------------------
# Statistics
# -------------------------

games = len(filtered)


wins = int(
    (filtered["Placement"] == 1)
    .sum()
)


average_place = (
    filtered["Placement"]
    .mean()
)


average_score = (
    filtered["Points"]
    .mean()
)


win_rate = (
    wins / games * 100
)


# -------------------------
# Overview
# -------------------------

st.subheader(
    "Overview"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    stat_card(
        "Games",
        games,
        "🎮"
    )


with c2:

    stat_card(
        "Average Place",
        f"{average_place:.2f}",
        "🏆"
    )


with c3:

    stat_card(
        "Average Score",
        f"{average_score:,.0f}",
        "⭐"
    )


with c4:

    stat_card(
        "Win Rate",
        f"{win_rate:.1f}%",
        "👑"
    )


st.divider()


# -------------------------
# Performance
# -------------------------

st.subheader(
    "Performance"
)


c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    stat_card(
        "Riichi",
        int(filtered["Riichi"].sum()),
        "🀄"
    )


with c2:

    stat_card(
        "Wins",
        int(filtered["Wins"].sum()),
        "🔥"
    )


with c3:

    stat_card(
        "Ron",
        int(filtered["Ron"].sum()),
        "🎯"
    )


with c4:

    stat_card(
        "Tsumo",
        int(filtered["Tsumo"].sum()),
        "⚡"
    )


with c5:

    stat_card(
        "Deal-ins",
        int(filtered["Deal-ins"].sum()),
        "💥"
    )


st.divider()


# -------------------------
# Recent matches
# -------------------------

st.subheader(
    "Recent Matches"
)


recent = (
    filtered
    .tail(5)
    .iloc[::-1]
    .copy()
)


recent["Placement"] = recent["Placement"].map(
    {
        1: "🥇 1st",
        2: "🥈 2nd",
        3: "🥉 3rd",
        4: "4th"
    }
)


st.dataframe(

    recent[
        [
            "Date",
            "Mode",
            "Placement",
            "Points",
            "Riichi",
            "Wins",
            "Deal-ins"
        ]
    ],

    hide_index=True,

    use_container_width=True

)
