def parse_replay(game, player_name):

    players = game["name"]

    player_id = players.index(player_name)

    # -------------------------
    # Starting scores
    # -------------------------

    scores = game["log"][0][1][:3].copy()

    riichi = 0
    wins = 0
    ron = 0
    tsumo = 0
    deal_ins = 0

    # -------------------------
    # Process hands
    # -------------------------

    for hand in game["log"]:

        # -------------------------
        # Riichi detection
        # -------------------------

        discard_index = 4 + player_id * 3 + 2

        if discard_index < len(hand):

            for tile in hand[discard_index]:

                if isinstance(tile, str) and tile.startswith("r"):

                    riichi += 1

        # -------------------------
        # Result
        # -------------------------

        result = hand[-1]

        if not isinstance(result, list):
            continue

        if result[0] != "和了":
            continue

        delta = result[1][:3]

        # update scores

        for i in range(3):

            scores[i] += delta[i]

        # -------------------------
        # Winner / Loser
        # -------------------------

        info = result[2]

        winner = info[0]
        loser = info[1]

        # -------------------------
        # I won
        # -------------------------

        if winner == player_id:

            wins += 1

            # same player = tsumo
            if winner == loser:

                tsumo += 1

            else:

                ron += 1

        # -------------------------
        # I dealt in
        # -------------------------

        elif loser == player_id:

            deal_ins += 1

    # -------------------------
    # Placement
    # -------------------------

    ranking = sorted(
        range(3),
        key=lambda x: scores[x],
        reverse=True
    )

    placement = ranking.index(player_id) + 1

    # -------------------------
    # Remove riichi sticks
    # -------------------------

    display_score = scores[player_id] - (riichi * 1000)

    return {

        "Player": player_name,

        "Placement": placement,

        "Points": display_score,

        "Riichi": riichi,

        "Wins": wins,

        "Ron": ron,

        "Tsumo": tsumo,

        "Deal-ins": deal_ins

    }
