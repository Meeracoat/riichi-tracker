import streamlit as st

from utils import sidebar_import


# -------------------------
# Page setup
# -------------------------

st.set_page_config(
    page_title="Riichi Tracker",
    page_icon="🀄",
    layout="wide"
)


# -------------------------
# Login state
# -------------------------

if "username" not in st.session_state:

    st.session_state.username = ""


# -------------------------
# Sidebar
# -------------------------

sidebar_import()


# -------------------------
# Pages
# -------------------------

dashboard = st.Page(
    "pages/dashboard.py",
    title="📊 Dashboard"
)


history = st.Page(
    "pages/match_history.py",
    title="📜 Match History"
)


trends = st.Page(
    "pages/trends.py",
    title="📈 Trends"
)

profile = st.Page(
    "pages/profile.py",
    title="👤 Profile"
)

leaderboard = st.Page(
    "pages/leaderboard.py",
    title="🏆 Leaderboard"
)

details = st.Page(
    "pages/match_details.py",
    title="🀄 Match Details"
)

replay_viewer = st.Page(
    "pages/replay_viewer.py",
    title="🎬 Replay Viewer"
)


# -------------------------
# Navigation
# -------------------------

pg = st.navigation(
    {
        "🀄 Riichi Tracker": [

            dashboard,

            history,

            trends,

            profile,

            leaderboard,

            details,
            
            replay_viewer

        ]
    }
)


pg.run()
