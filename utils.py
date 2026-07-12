import streamlit as st

from api import get_replay
from parser import parse_replay
from storage import save_match


def sidebar_import():

    st.sidebar.header(
        "🀄 Riichi Tracker"
    )

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
    # Replay Import
    # -------------------------

    st.sidebar.header(

        "📥 Import Replay"

    )

    replay_id = st.sidebar.text_input(

        "Riichi City Replay ID"

    )

    if st.sidebar.button(

        "Import Replay"

    ):

        replay_id = replay_id.strip()

        if replay_id == "":

            st.sidebar.warning(

                "Enter a replay ID."

            )

            return

        try:

            # Get replay JSON

            game = get_replay(

                replay_id

            )

            # Check player exists

            if username not in game["name"]:

                st.sidebar.error(

                    f"{username} was not found in this replay."

                )

                return

            # Parse stats

            stats = parse_replay(

                game,

                username

            )

            # -------------------------
            # Add replay information
            # -------------------------

            stats["Replay"] = replay_id

            stats["ReplayData"] = game

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

            # Save

            saved = save_match(

                stats,

                username

            )

            if saved:

                st.sidebar.success(

                    "Replay imported!"

                )

            else:

                st.sidebar.warning(

                    "Replay already imported."

                )

            st.rerun()

        except Exception as e:

            st.sidebar.error(

                "Failed to import replay."

            )

            st.sidebar.exception(e)
