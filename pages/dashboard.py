import streamlit as st
import pandas as pd

from storage import load_matches


st.title("📊 Dashboard")


# -------------------------
# Check username
# -------------------------

username = st.session_state.get(
    "username",
    ""
)


if username == "":

    st.info(
        "👤 Enter your username in the sidebar first."
    )

    st.stop()


# -------------------------
# Load user matches
# -------------------------

matches = load_matches(
    username
)


# -------------------------
# Empty state
# -------------------------

if not matches:

    st.info(
        f"🀄 No games recorded for {username} yet.\n\n"
        "Import a replay from the sidebar."
    )

    st.stop()


df = pd.DataFrame(matches)


# -------------------------
# Stats
# -------------------------

st.subheader(
    f"📊 {username}'s Stats"
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "🎮 Games",
    len(df)
)


c2.metric(
    "📍 Average Place",
    f'{df["Placement"].mean():.2f}'
)


c3.metric(
    "💴 Average Score",
    f'{df["Points"].mean():,.0f}'
)


c4.metric(
    "📊 Sum of Places",
    int(df["Placement"].sum())
)


st.divider()


# -------------------------
# Placement stats
# -------------------------

st.subheader(
    "Placements"
)


c1, c2, c3 = st.columns(3)


c1.metric(
    "🥇 1st",
    len(df[df["Placement"] == 1])
)


c2.metric(
    "🥈 2nd",
    len(df[df["Placement"] == 2])
)


c3.metric(
    "🥉 3rd",
    len(df[df["Placement"] == 3])
)


st.divider()


# -------------------------
# Game stats
# -------------------------

st.subheader(
    "Game Statistics"
)


c1, c2, c3, c4 = st.columns(4)


c1.metric(
    "🀄 Riichi",
    int(df["Riichi"].sum())
)


c2.metric(
    "🔥 Wins",
    int(df["Wins"].sum())
)


c3.metric(
    "🎯 Ron",
    int(df["Ron"].sum())
)


c4.metric(
    "💥 Deal-ins",
    int(df["Deal-ins"].sum())
)
