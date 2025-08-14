import pulp
import polars as pl

from fpl.repositories import PlayerRepository
from fpl.repositories import PlayerTypeRepository
from fpl.repositories import TeamRepository

def is_valid_squad(squad):
    total_cost = sum(p['player_cost'] for p in squad)
    if total_cost > 1000:
        return False
    team_counts = {}
    for p in squad:
        team_counts[p['team_name']] = team_counts.get(p['team_name'], 0) + 1
        if team_counts[p['team_name']] > 3:
            return False
    return True

if __name__ == "__main__":
    print("Running main program...")

    player_repo = PlayerRepository()
    player_list = player_repo.get_all()
    player_df = pl.DataFrame(player_list)

    team_repo = TeamRepository()
    team_list = team_repo.get_all()
    team_df = pl.DataFrame(team_list)

    pt_repo = PlayerTypeRepository()
    pt_list = pt_repo.get_all()
    pt_df = pl.DataFrame(pt_list)
    
    print("0: Player DataFrame schema:", player_df)

    player_df = player_df.select([
        pl.col("id").alias("player_id"),
        pl.col("code").alias("player_code"),
        (pl.col("first_name") + " " + pl.col("second_name")).alias("player_full_name"),
        pl.col("element_type").alias("player_type_id"),
        pl.col("now_cost").alias("player_cost"),
        pl.col("team").alias("team_id"),
        pl.col("expected_goals_per_90"),
        pl.col("expected_assists_per_90"),
        pl.col("expected_goal_involvements_per_90"),
        pl.col("expected_goals_conceded_per_90")
    ])

    team_df = team_df.select([
        pl.col("id").alias("team_id"),
        pl.col("code").alias("team_code"),
        pl.col("name").alias("team_name"),
        pl.col("short_name").alias("team_short_name"),
        # pl.col("strength_overall_home"),
        # pl.col("strength_overall_away"),
        # pl.col("strength_attack_home"),
        # pl.col("strength_attack_away"),
        # pl.col("strength_defence_home"),
        # pl.col("strength_defence_away"),
        ((pl.col("strength_attack_home") * pl.col("strength_attack_away")) / 2).alias("strength_attack_overall"),
        ((pl.col("strength_defence_home") * pl.col("strength_defence_away")) / 2).alias("strength_defence_overall"),
    ])

    pt_df = pt_df.select([
        pl.col("id").alias("player_type_id"),
        pl.col("singular_name_short").alias("player_type"),
        pl.col("squad_select").alias("num_to_select")
    ])

    print("1: Player DataFrame schema:", player_df.schema)

    player_df = player_df.join(
        pt_df,
        on="player_type_id",
        how="inner"
    )
    print("2: Player DataFrame schema:", player_df.schema)

    player_df = player_df.join(
        team_df,
        on="team_id",
        how="inner"
    )
    print("3: Player DataFrame schema:", player_df.schema)

    player_df = player_df.filter(
        ((pl.col("player_type").is_in(["GKP", "DEF"])) &
        (pl.col("expected_goals_conceded_per_90") > 0))
        |
        (pl.col("player_type").is_in(["MID", "FWD"]))
    )
    print("4: Player DataFrame schema:", player_df.schema)

    final_player_df = player_df.with_columns([
        pl.when(pl.col("player_type") == "GKP")
            .then((20 - pl.col("expected_goals_conceded_per_90")) * pl.col("strength_defence_overall"))
            .when(pl.col("player_type") == "DEF")
            .then(((20 - pl.col("expected_goals_conceded_per_90")) * pl.col("strength_defence_overall")) + (pl.col("expected_goal_involvements_per_90") * pl.col("strength_attack_overall")))
            .when(pl.col("player_type") == "MID")
            .then(pl.col("expected_goal_involvements_per_90") * pl.col("strength_attack_overall"))
            .otherwise(pl.col("expected_goals_per_90") * pl.col("strength_attack_overall"))
            .alias("computed_score")
    ]).select([
        pl.col("player_id"),
        pl.col("player_full_name"),
        pl.col("player_cost"),
        pl.col("player_type"),
        pl.col("team_name"),
        pl.col("computed_score")
    ])
    print("5: Final player DataFrame schema:", final_player_df.schema)
    print("5: Final player DataFrame:", final_player_df)

    normalised_player_df = final_player_df.with_columns([
        (
            (pl.col("computed_score") - pl.col("computed_score").min().over("player_type")) /
            (pl.col("computed_score").max().over("player_type") - pl.col("computed_score").min().over("player_type"))
        ).alias("normalised_score")
    ])

    print("6: Normalised player DataFrame schema:", normalised_player_df.schema)
    print("6: Normalised player DataFrame:", normalised_player_df)

    players = normalised_player_df.to_dicts()

    # Define LP problem
    prob = pulp.LpProblem("FPL_Squad_Selection", pulp.LpMaximize)

    # Create binary variables: 1 if player is selected, 0 otherwise
    player_vars = {p['player_id']: pulp.LpVariable(f"x_{p['player_id']}", cat='Binary') for p in players}

    # Objective: maximize total normalized score
    prob += pulp.lpSum([p['normalised_score'] * player_vars[p['player_id']] for p in players])

    # Constraints
    # 1. Total players = 15
    prob += pulp.lpSum(player_vars.values()) == 15

    # 2. Position constraints
    prob += pulp.lpSum([player_vars[p['player_id']] for p in players if p['player_type']=="GKP"]) == 2
    prob += pulp.lpSum([player_vars[p['player_id']] for p in players if p['player_type']=="DEF"]) == 5
    prob += pulp.lpSum([player_vars[p['player_id']] for p in players if p['player_type']=="MID"]) == 5
    prob += pulp.lpSum([player_vars[p['player_id']] for p in players if p['player_type']=="FWD"]) == 3

    # 3. Max 3 players per team
    teams = set(p['team_name'] for p in players)
    for team in teams:
        prob += pulp.lpSum([player_vars[p['player_id']] for p in players if p['team_name']==team]) <= 3

    # 4. Total cost <= 1000
    prob += pulp.lpSum([p['player_cost'] * player_vars[p['player_id']] for p in players]) <= 1000

    top_squads = []

    for k in range(5):
        # Solve
        prob.solve()
        
        if pulp.LpStatus[prob.status] != "Optimal":
            break
        
        # Get selected players
        selected = [p for p in players if player_vars[p['player_id']].varValue == 1]
        total_score = sum(p['normalised_score'] for p in selected)
        
        top_squads.append((total_score, selected))
        
        # Exclude this squad in next iteration
        prob += pulp.lpSum([player_vars[p['player_id']] for p in selected]) <= 14  # Must change at least 1 player

    # Display top squads
    pl.Config.set_tbl_rows(15)
    for i, (score, squad) in enumerate(top_squads):
        print(f"\nTop Squad #{i+1} - Total Score: {score}")
        squad_df = pl.DataFrame(squad)
        print(squad_df)
