import streamlit as st
import pandas as pd

from storage import load_all_matches


st.title("🏆 Leaderboard")


# -------------------------
# Load matches
# -------------------------

matches = load_all_matches()


if not matches:

    st.info(
        "No matches recorded yet."
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
# Build leaderboard
# -------------------------

leaderboard = (

    filtered

    .groupby("Username")

    .agg(

        Games=("Placement", "count"),

        Average_Place=("Placement", "mean"),

        Average_Score=("Points", "mean"),

        Wins=("Placement",
              lambda x:
              (x == 1).sum()
              ),

        Riichi=("Riichi", "sum")

    )

    .reset_index()

)


leaderboard["Win Rate"] = (

    leaderboard["Wins"]

    /

    leaderboard["Games"]

    *

    100

)


# -------------------------
# Sorting
# -------------------------

sort = st.selectbox(

    "Sort by",

    [

        "Average Place",

        "Win Rate",

        "Average Score",

        "Games"

    ]

)


if sort == "Average Place":

    leaderboard = leaderboard.sort_values(

        "Average_Place"

    )


elif sort == "Win Rate":

    leaderboard = leaderboard.sort_values(

        "Win Rate",

        ascending=False

    )


elif sort == "Average Score":

    leaderboard = leaderboard.sort_values(

        "Average_Score",

        ascending=False

    )


elif sort == "Games":

    leaderboard = leaderboard.sort_values(

        "Games",

        ascending=False

    )


# -------------------------
# Display
# -------------------------

st.divider()


display = leaderboard.copy()


display["Average_Place"] = display[
    "Average_Place"
].round(2)


display["Average_Score"] = display[
    "Average_Score"
].round(0)


display["Win Rate"] = (

    display["Win Rate"]

    .round(1)

    .astype(str)

    + "%"

)


display = display.rename(

    columns={

        "Username":
            "Player",

        "Average_Place":
            "Average Place",

        "Average_Score":
            "Average Score"

    }

)


st.dataframe(

    display[

        [

            "Player",

            "Games",

            "Average Place",

            "Average Score",

            "Wins",

            "Win Rate",

            "Riichi"

        ]

    ],

    hide_index=True,

    use_container_width=True

)
