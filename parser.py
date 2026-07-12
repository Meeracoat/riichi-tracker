def parse_replay(game, player_name):

    players = game["name"]

    player_id = players.index(player_name)

    player_count = len(players)

    # -------------------------
    # Starting scores
    # -------------------------

    scores = game["log"][0][1][:player_count].copy()

    # -------------------------
    # Stats
    # -------------------------

    riichi = 0
    wins = 0
    ron = 0
    tsumo = 0
    deal_ins = 0

    # -------------------------
    # Process rounds
    # -------------------------

    for hand in game["log"]:

        # Skip broken rounds

        if len(hand) < 2:
            continue

        # -------------------------
        # Count riichi
        # -------------------------

        for section in hand:

            if isinstance(section, list):

                for tile in section:

                    if isinstance(tile, str):

                        if tile.startswith("r"):

                            riichi += 1

        result = hand[-1]

        if not isinstance(result, list):
            continue

        # -------------------------
        # Apply score change
        # -------------------------

        if result[0] in ["和了", "流局"]:

            delta = result[1]

            for i in range(player_count):

                scores[i] += delta[i]

        # -------------------------
        # Win / loss tracking
        # -------------------------

        if result[0] != "和了":

            continue

        info = result[2]

        winner = info[0]

        loser = info[1]

        if winner == player_id:

            wins += 1

            # tsumo

            if winner == loser:

                tsumo += 1

            # ron

            else:

                ron += 1

        elif loser == player_id:

            deal_ins += 1

    # -------------------------
    # Placement
    # -------------------------

    ranking = sorted(

        range(player_count),

        key=lambda x: scores[x],

        reverse=True

    )

    placement = ranking.index(player_id) + 1

    # -------------------------
    # Return
    # -------------------------

    return {

        "Player": player_name,

        "Placement": placement,

        "Points": scores[player_id],

        "Riichi": riichi,

        "Wins": wins,

        "Ron": ron,

        "Tsumo": tsumo,

        "Deal-ins": deal_ins,

        "Players": player_count

    }
