import streamlit as st
import pandas as pd

from storage import load_matches


st.title("📜 Match History")


username = st.session_state.get(
    "username",
    ""
)


if username == "":

    st.info(
        "Enter your username in the sidebar."
    )

    st.stop()


matches = load_matches(username)


if not matches:

    st.info(
        "No games imported yet."
    )

    st.stop()


df = pd.DataFrame(matches)


st.subheader("Filters")


filtered = df.copy()


c1, c2, c3 = st.columns(3)


with c1:

    placement_filter = st.multiselect(
        "Placement",
        sorted(filtered["Placement"].unique())
    )


with c2:

    mode_filter = st.multiselect(
        "Mode",
        filtered["Mode"].unique()
    )


with c3:

    result_filter = st.selectbox(
        "Result",
        [
            "All",
            "Wins",
            "Losses"
        ]
    )


if placement_filter:

    filtered = filtered[
        filtered["Placement"].isin(
            placement_filter
        )
    ]


if mode_filter:

    filtered = filtered[
        filtered["Mode"].isin(
            mode_filter
        )
    ]


if result_filter == "Wins":

    filtered = filtered[
        filtered["Placement"] == 1
    ]


elif result_filter == "Losses":

    filtered = filtered[
        filtered["Placement"] != 1
    ]


st.divider()

st.subheader("Matches")


for index, row in filtered.iterrows():

    placement = {
        1: "🥇 1st",
        2: "🥈 2nd",
        3: "🥉 3rd",
        4: "4th"
    }.get(
        row["Placement"],
        row["Placement"]
    )

    with st.container(border=True):

        st.write(
            f"**{row['Date']}**"
        )

        st.write(
            f"{row['Mode']} | {placement} | {row['Points']:,} pts"
        )

        if st.button(
            "View Match",
            key=f"match_{index}"
        ):

            st.session_state.selected_match = row.to_dict()

            st.switch_page(
                "pages/match_details.py"
            )
