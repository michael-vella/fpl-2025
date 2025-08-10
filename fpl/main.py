import polars as pl

from fpl.repositories import PlayerRepository
from fpl.repositories import TeamRepository


if __name__ == "__main__":
    print("Running main program...")

    player_repo = PlayerRepository()
    player_list = player_repo.get_all()
    player_df = pl.DataFrame(player_list)

    team_repo = TeamRepository()
    team_list = team_repo.get_all()
    team_df = pl.DataFrame(team_list)
    
    print(f"Team schema: '{team_df.schema}'")
    print(f"Player schema: '{player_df.schema}'")

    joined_df = player_df.join(
        team_df,
        left_on="team",
        right_on="id",
        how="inner"
    )

    print(team_df)
    print(player_df)

    print(joined_df)
