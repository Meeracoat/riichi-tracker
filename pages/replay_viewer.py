import streamlit as st
import re


st.title("🎬 Replay Viewer")


# -------------------------
# Yaku translations
# -------------------------

YAKU_TRANSLATIONS = {

    "立直": "Riichi",

    "門前清自摸和": "Menzen Tsumo",

    "平和": "Pinfu",

    "混一色": "Honitsu (Half Flush)",

    "清一色": "Chinitsu (Full Flush)",

    "役牌": "Yakuhai (Value Tile)",

    "ドラ": "Dora",

    "裏ドラ": "Ura Dora",

    "一発": "Ippatsu",

    "七対子": "Chiitoitsu (Seven Pairs)",

    "断么九": "Tanyao",

    "三色同順": "Sanshoku",

    "三暗刻": "Sanankou",

    "対々和": "Toitoi",

    "国士無双": "Kokushi Musou",

    "大三元": "Daisangen",

    "小三元": "Shousangen",

    "四暗刻": "Suuankou",

    "混老頭": "Honroutou",

    "純全帯么九": "Junchan",

    "混全帯么九": "Chanta"

}


def translate_yaku(text):

    for jp, en in YAKU_TRANSLATIONS.items():

        if text.startswith(jp):

            return text.replace(
                jp,
                en
            )

    return text


# -------------------------
# Load match
# -------------------------
if "selected_match" not in st.session_state:

    st.info(
        "Select a match first."
    )

    st.stop()


match = st.session_state.selected_match


replay = match.get(
    "ReplayData"
)


if replay is None:

    st.warning(
        "No replay data found."
    )

    st.stop()


players = replay["name"]

logs = replay["log"]


# -------------------------
# Valid rounds
# -------------------------

rounds = []


for hand in logs:

    if (
        isinstance(hand, list)
        and len(hand) >= 5
        and isinstance(hand[-1], list)
    ):

        rounds.append(hand)


if not rounds:

    st.error(
        "No rounds found."
    )

    st.stop()


# -------------------------
# Round names
# -------------------------

def get_round_name(index, hand):

    wind_number = index

    if len(players) == 4:

        winds = [

            "East",

            "South",

            "West",

            "North"

        ]

    else:

        winds = [

            "East",

            "South"

        ]

    # Riichi City logs are sequential

    round_wind = winds[
        wind_number // 4
        if len(players) == 4
        else wind_number // 3
    ]

    number = (

        wind_number %

        (4 if len(players) == 4 else 3)

    ) + 1

    return f"{round_wind} {number}"


round_names = [

    get_round_name(i, hand)

    for i, hand in enumerate(rounds)

]


# -------------------------
# Select round
# -------------------------

choice = st.selectbox(

    "Round",

    range(len(rounds)),

    format_func=lambda x:
        round_names[x]

)


hand = rounds[choice]


st.subheader(
    round_names[choice]
)


# -------------------------
# Scores
# -------------------------

scores = hand[1]


cols = st.columns(
    len(players)
)


for i, player in enumerate(players):

    cols[i].metric(

        player,

        scores[i]

    )


st.divider()


# -------------------------
# Result
# -------------------------

result = hand[-1]


if result[0] == "和了":

    st.success(
        "🏆 Win"
    )

    changes = result[1]

    for i, player in enumerate(players):

        st.write(

            f"{player}: {changes[i]:+}"

        )

    st.subheader(
        "Yaku"
    )

    for item in result[2][3:]:

        st.write(

            "⭐ " +
            translate_yaku(item)

        )


elif result[0] == "流局":

    st.warning(
        "Draw"
    )

else:

    st.info(
        result[0]
    )
