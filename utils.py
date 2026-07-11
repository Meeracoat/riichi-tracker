import streamlit as st

from api import get_replay
from parser import parse_replay
from storage import save_match


def sidebar_import():

    st.sidebar.header("🀄 Riichi Tracker")

    # -------------------------
    # Username
    # -------------------------

    username = st.sidebar.text_input(
        "Username",
        value=st.session_state.username
    )


    st.session_state.username = username

    if username.strip() == "":

        st.sidebar.info(
            "Enter your username first."
        )

        return

    st.sidebar.divider()

    # -------------------------
    # Replay import
    # -------------------------

    st.sidebar.header(
        "📥 Import Replay"
    )

    replay_id = st.sidebar.text_input(
        "Riichi City Replay ID"
    )

    if st.sidebar.button("Import Replay"):

        replay_id = replay_id.strip()

        if replay_id == "":

            st.sidebar.warning(
                "Enter a replay ID."
            )

            return

        try:

            game = get_replay(
                replay_id
            )

            if username not in game["name"]:

                st.sidebar.error(
                    f"{username} was not found in this replay."
                )

                return

            stats = parse_replay(
                game,
                username
            )

            stats["Replay"] = replay_id

            stats["Date"] = (
                game
                .get(
                    "title",
                    [
                        "Unknown",
                        "Unknown"
                    ]
                )[1]
            )

            stats["Mode"] = (
                game
                .get(
                    "title",
                    [
                        "Unknown"
                    ]
                )[0]
            )

            save_match(
                stats,
                username
            )

            st.sidebar.success(
                "Replay imported!"
            )

            st.rerun()

        except Exception as e:

            st.sidebar.error(
                "Failed to import replay."
            )

            st.sidebar.exception(e)
