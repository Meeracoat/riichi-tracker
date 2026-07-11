import streamlit as st
import pandas as pd

from storage import load_matches


st.title("📜 Match History")


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


# -------------------------
# Empty state
# -------------------------

if not matches:

    st.info(
        f"🀄 No matches recorded for {username} yet."
    )

    st.stop()


df = pd.DataFrame(matches)


# -------------------------
# Format
# -------------------------

df["Placement"] = df["Placement"].map(
    {
        1: "🥇 1st",
        2: "🥈 2nd",
        3: "🥉 3rd"
    }
)


df["Points"] = df["Points"].apply(
    lambda x: f"{x:,}"
)


# newest first

df = df.iloc[::-1]


# -------------------------
# Display
# -------------------------

st.subheader(
    f"📜 {username}'s Matches"
)


st.dataframe(

    df[
        [
            "Date",
            "Mode",
            "Placement",
            "Points",
            "Riichi",
            "Wins",
            "Ron",
            "Tsumo",
            "Deal-ins"
        ]
    ],

    use_container_width=True,

    hide_index=True
)
