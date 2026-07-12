import streamlit as st
import pandas as pd

from storage import load_matches


st.title("👤 Profile")


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
# Stats function
# -------------------------

def get_stats(data):

    if data.empty:

        return {

            "games": 0,
            "average_place": 0,
            "average_score": 0,
            "wins": 0,
            "riichi": 0,
            "highest": 0,
            "best": "-"

        }

    return {

        "games":
            len(data),


        "average_place":
            data["Placement"].mean(),


        "average_score":
            data["Points"].mean(),


        "wins":
            int(
                (data["Placement"] == 1)
                .sum()
            ),


        "riichi":
            int(
                data["Riichi"].sum()
            ),


        "highest":
            int(
                data["Points"].max()
            ),


        "best":
            int(
                data["Placement"].min()
            )

    }


# -------------------------
# Split formats
# -------------------------
all_stats = get_stats(df)


sanma = df[
    df["Players"] == 3
]


yonma = df[
    df["Players"] == 4
]


sanma_stats = get_stats(
    sanma
)


yonma_stats = get_stats(
    yonma
)


# -------------------------
# Player name
# -------------------------

st.subheader(
    username
)


# -------------------------
# Overall
# -------------------------

st.divider()

st.subheader(
    "Overall"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "🎮 Games",
        all_stats["games"]
    )


with c2:

    st.metric(
        "🏆 Average Place",
        f"{all_stats['average_place']:.2f}"
    )


with c3:

    st.metric(
        "⭐ Average Score",
        f"{all_stats['average_score']:,.0f}"
    )


with c4:

    winrate = (
        all_stats["wins"]
        /
        all_stats["games"]
        *
        100
    )

    st.metric(
        "👑 Win Rate",
        f"{winrate:.1f}%"
    )


# -------------------------
# Sanma
# -------------------------

if not sanma.empty:

    st.divider()

    st.subheader(
        "🀄 3 Player Stats"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🎮 Games",
            sanma_stats["games"]
        )

    with c2:

        st.metric(
            "🏆 Average Place",
            f"{sanma_stats['average_place']:.2f}"
        )

    with c3:

        st.metric(
            "🔥 Wins",
            sanma_stats["wins"]
        )

    with c4:

        st.metric(
            "🀄 Riichi",
            sanma_stats["riichi"]
        )


# -------------------------
# Yonma
# -------------------------

if not yonma.empty:

    st.divider()

    st.subheader(
        "🀄 4 Player Stats"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(
            "🎮 Games",
            yonma_stats["games"]
        )

    with c2:

        st.metric(
            "🏆 Average Place",
            f"{yonma_stats['average_place']:.2f}"
        )

    with c3:

        st.metric(
            "🔥 Wins",
            yonma_stats["wins"]
        )

    with c4:

        st.metric(
            "🀄 Riichi",
            yonma_stats["riichi"]
        )


# -------------------------
# Records
# -------------------------

st.divider()

st.subheader(
    "🏆 Records"
)


c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        "🚀 Highest Score",
        f"{all_stats['highest']:,}"
    )


with c2:

    st.metric(
        "🥇 Best Placement",
        all_stats["best"]
    )


with c3:

    st.metric(
        "🔥 Total Wins",
        all_stats["wins"]
    )


with c4:

    st.metric(
        "🀄 Total Riichi",
        all_stats["riichi"]
    )
