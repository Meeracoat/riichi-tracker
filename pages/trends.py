import streamlit as st
import pandas as pd
import plotly.express as px

from storage import load_matches


st.title("📈 Trends")


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
# Compatibility
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
# Add game number
# -------------------------

filtered = filtered.reset_index(
    drop=True
)


filtered["Game"] = (
    filtered.index + 1
)


# -------------------------
# Score trend
# -------------------------

st.divider()

st.subheader(
    "⭐ Score Trend"
)


fig = px.line(

    filtered,

    x="Game",

    y="Points",

    markers=True,

    title="Score over games"

)


st.plotly_chart(
    fig,
    use_container_width=True
)


# -------------------------
# Placement trend
# -------------------------

st.divider()

st.subheader(
    "🏆 Placement Trend"
)


fig = px.line(

    filtered,

    x="Game",

    y="Placement",

    markers=True,

    title="Placement over games"

)


fig.update_yaxes(
    autorange="reversed"
)


st.plotly_chart(

    fig,

    use_container_width=True

)


# -------------------------
# Win rate
# -------------------------

st.divider()

st.subheader(
    "👑 Win Rate"
)


wins = (
    filtered["Placement"] == 1
).sum()


games = len(filtered)


win_rate = (
    wins / games * 100
)


st.metric(

    "Win Rate",

    f"{win_rate:.1f}%"

)


# -------------------------
# Riichi trend
# -------------------------

st.divider()

st.subheader(
    "🀄 Riichi"
)


fig = px.bar(

    filtered,

    x="Game",

    y="Riichi",

    title="Riichi calls"

)


st.plotly_chart(

    fig,

    use_container_width=True

)
