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


# -------------------------
# Navigation
# -------------------------

pg = st.navigation(
    {
        "🀄 Riichi Tracker": [

            dashboard,

            history,

            trends

        ]
    }
)


pg.run()
