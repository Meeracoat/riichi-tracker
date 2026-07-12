import streamlit as st


st.title("🀄 Match Details")


# -------------------------
# Check selected match
# -------------------------

if "selected_match" not in st.session_state:

    st.info(
        "Select a match from Match History."
    )

    st.stop()


match = st.session_state.selected_match


# -------------------------
# Helpers
# -------------------------

placement_names = {

    1: "🥇 1st",

    2: "🥈 2nd",

    3: "🥉 3rd",

    4: "4th"

}


placement = placement_names.get(

    match["Placement"],

    match["Placement"]

)


players = match.get(

    "Players",

    3

)


format_name = (

    "🀄 Sanma (3 Player)"

    if players == 3

    else

    "🀄 Yonma (4 Player)"

)


# -------------------------
# Header
# -------------------------

st.subheader(

    match["Mode"]

)


c1, c2 = st.columns(2)


with c1:

    st.write(

        f"📅 {match['Date']}"

    )


with c2:

    st.write(

        format_name

    )


st.divider()


# -------------------------
# Main Stats
# -------------------------

c1, c2, c3 = st.columns(3)


with c1:

    st.metric(

        "Placement",

        placement

    )


with c2:

    st.metric(

        "Score",

        f"{match['Points']:,}"

    )


with c3:

    st.metric(

        "Replay",

        match["Replay"]

    )


st.divider()


# -------------------------
# Performance
# -------------------------

st.subheader(

    "Performance"

)


c1, c2, c3, c4, c5 = st.columns(5)


with c1:

    st.metric(

        "🀄 Riichi",

        match["Riichi"]

    )


with c2:

    st.metric(

        "🔥 Wins",

        match["Wins"]

    )


with c3:

    st.metric(

        "🎯 Ron",

        match["Ron"]

    )


with c4:

    st.metric(

        "⚡ Tsumo",

        match["Tsumo"]

    )


with c5:

    st.metric(

        "💥 Deal-ins",

        match["Deal-ins"]

    )


st.divider()


# -------------------------
# Quick Summary
# -------------------------

st.subheader(

    "Summary"

)


if match["Placement"] == 1:

    st.success(

        "🏆 Victory!"

    )


elif match["Placement"] == players:

    st.error(

        "💀 Last place"

    )


else:

    st.info(

        "Good game!"

    )


st.divider()


# -------------------------
# Replay
# -------------------------

st.subheader(

    "Replay ID"

)


st.code(

    match["Replay"]

)


if st.button(

    "⬅ Back to Match History"

):

    st.switch_page(

        "pages/match_history.py"

    )

if st.button(
    "🎬 View Replay"
):

    st.switch_page(
        "pages/replay_viewer.py"
    )
