import streamlit as st

from supabase import create_client


# -------------------------
# Supabase connection
# -------------------------

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)


# -------------------------
# Users
# -------------------------

def get_user(username):

    result = (
        supabase
        .table("users")
        .select("id")
        .eq(
            "username",
            username
        )
        .execute()
    )

    if result.data:

        return result.data[0]["id"]

    return None


def create_user(username):

    user_id = get_user(username)

    if user_id:

        return user_id

    result = (
        supabase
        .table("users")
        .insert(
            {
                "username": username
            }
        )
        .execute()
    )

    return result.data[0]["id"]


# -------------------------
# Save Match
# -------------------------

def save_match(match, username):

    user_id = create_user(
        username
    )

    # -------------------------
    # Duplicate check
    # -------------------------

    existing = (

        supabase

        .table("matches")

        .select("id")

        .eq(
            "user_id",
            user_id
        )

        .eq(
            "replay",
            match["Replay"]
        )

        .execute()

    )

    if existing.data:

        return False

    # -------------------------
    # Match data
    # -------------------------

    data = {


        "user_id":

            user_id,


        "replay":

            match["Replay"],


        "date":

            match["Date"],


        "mode":

            match["Mode"],


        "placement":

            match["Placement"],


        "points":

            match["Points"],


        "riichi":

            match["Riichi"],


        "wins":

            match["Wins"],


        "ron":

            match["Ron"],


        "tsumo":

            match["Tsumo"],


        "deal_ins":

            match["Deal-ins"],


        "players":

            match.get(
                "Players",
                3
            ),


        "replay_data":

            match.get(
                "ReplayData"
            )

    }

    supabase.table("matches").insert(data).execute()

    return True


# -------------------------
# Load Player Matches
# -------------------------

def load_matches(username):

    user_id = get_user(
        username
    )

    if user_id is None:

        return []

    result = (

        supabase

        .table("matches")

        .select("*")

        .eq(
            "user_id",
            user_id
        )

        .order(
            "id"
        )

        .execute()

    )

    matches = []

    for row in result.data:

        matches.append({

            "Replay":

                row["replay"],


            "Date":

                row["date"],


            "Mode":

                row["mode"],


            "Placement":

                row["placement"],


            "Points":

                row["points"],


            "Riichi":

                row["riichi"],


            "Wins":

                row["wins"],


            "Ron":

                row["ron"],


            "Tsumo":

                row["tsumo"],


            "Deal-ins":

                row["deal_ins"],


            "Players":

                row.get(
                    "players",
                    3
                ),


            "ReplayData":

                row.get(
                    "replay_data"
                )

        })

    return matches


# -------------------------
# Load All Matches
# -------------------------

def load_all_matches():

    matches_result = (

        supabase

        .table("matches")

        .select("*")

        .execute()

    )

    users_result = (

        supabase

        .table("users")

        .select("*")

        .execute()

    )

    user_map = {

        user["id"]:
            user["username"]

        for user in users_result.data

    }

    matches = []

    for row in matches_result.data:

        matches.append({

            "Username":

                user_map.get(

                    row["user_id"],

                    "Unknown"

                ),


            "Replay":

                row["replay"],


            "Placement":

                row["placement"],


            "Points":

                row["points"],


            "Riichi":

                row["riichi"],


            "Wins":

                row["wins"],


            "Ron":

                row["ron"],


            "Tsumo":

                row["tsumo"],


            "Deal-ins":

                row["deal_ins"],


            "Players":

                row.get(
                    "players",
                    3
                ),


            "ReplayData":

                row.get(
                    "replay_data"
                )

        })

    return matches
