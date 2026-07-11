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
        .eq("username", username)
        .execute()
    )

    if result.data:

        return result.data[0]["id"]

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
# Save match
# -------------------------

def save_match(match, username):

    user_id = get_user(username)

    # -------------------------
    # Check duplicate
    # -------------------------

    existing = (
        supabase
        .table("matches")
        .select("id")
        .eq("user_id", user_id)
        .eq("replay", match["Replay"])
        .execute()
    )


    if existing.data:

        return False


    # -------------------------
    # Insert new match
    # -------------------------

    data = {

        "user_id": user_id,

        "replay": match["Replay"],

        "date": match["Date"],

        "mode": match["Mode"],

        "placement": match["Placement"],

        "points": match["Points"],

        "riichi": match["Riichi"],

        "wins": match["Wins"],

        "ron": match["Ron"],

        "tsumo": match["Tsumo"],

        "deal_ins": match["Deal-ins"]

    }


    supabase.table("matches").insert(data).execute()


    return True


# -------------------------
# Load matches
# -------------------------

def load_matches(username):

    user_id = get_user(username)

    result = (
        supabase
        .table("matches")
        .select("*")
        .eq("user_id", user_id)
        .order("id")
        .execute()
    )

    matches = []

    for row in result.data:

        matches.append({

            "Replay": row["replay"],

            "Date": row["date"],

            "Mode": row["mode"],

            "Placement": row["placement"],

            "Points": row["points"],

            "Riichi": row["riichi"],

            "Wins": row["wins"],

            "Ron": row["ron"],

            "Tsumo": row["tsumo"],

            "Deal-ins": row["deal_ins"]

        })

    return matches
