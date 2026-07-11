import streamlit as st
import pandas as pd
import plotly.express as px

from storage import load_matches


st.title("📈 Trends")


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
# Load matches
# -------------------------

matches = load_matches(
    username
)


if not matches:

    st.info(
        f"🀄 No matches recorded for {username} yet."
    )

    st.stop()


df = pd.DataFrame(matches)


# -------------------------
# Last 10 games
# -------------------------

df = df.tail(10).reset_index(
    drop=True
)


df["Game"] = range(
    1,
    len(df) + 1
)


st.subheader(
    f"📈 Last 10 Matches - {username}"
)


# -------------------------
# Summary
# -------------------------

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
# Placement count
# -------------------------

st.subheader(
    "Placement Breakdown"
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
# Placement graph
# -------------------------

st.subheader(
    "Placement Trend"
)


fig = px.line(
    df,
    x="Game",
    y="Placement",
    markers=True
)


fig.update_yaxes(
    autorange="reversed",
    tickvals=[
        1,
        2,
        3
    ],
    ticktext=[
        "🥇 1st",
        "🥈 2nd",
        "🥉 3rd"
    ]
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -------------------------
# Score graph
# -------------------------

st.subheader(
    "Score Trend"
)


fig2 = px.line(
    df,
    x="Game",
    y="Points",
    markers=True
)


st.plotly_chart(
    fig2,
    use_container_width=True
)


# -------------------------
# Raw data
# -------------------------

with st.expander(
    "Show last 10 games"
):

    st.dataframe(

        df[
            [
                "Game",
                "Placement",
                "Points",
                "Riichi",
                "Wins",
                "Ron",
                "Tsumo",
                "Deal-ins"
            ]
        ],

        hide_index=True

    )
