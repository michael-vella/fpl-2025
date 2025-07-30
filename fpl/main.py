from api.client import APIClient
from services.data_parser import DataParser

if __name__ == "__main__":

    # start: to use repository pattern
    client = APIClient()
    bootstrap_data = client.get_data("bootstrap-static/")
    fixture_data = client.get_data("fixtures/")

    player_list = DataParser.extract_players(bootstrap_data)
    team_list = DataParser.extract_teams(bootstrap_data)
    player_type_list = DataParser.extract_player_types(bootstrap_data)
    gameweek_list = DataParser.extract_gameweeks(bootstrap_data)
    fixture_list = DataParser.extract_fixtures(fixture_data)
    # end to use repository pattern later

    print("\nPlayer List:")
    print(player_list[0])
    print(len(player_list))

    print("\nTeam List:")
    print(team_list[0])
    print(len(team_list))

    print("\nPlayer Type List:")
    print(player_type_list[0])
    print(len(player_type_list))

    print("\nGameweek List:")
    print(gameweek_list[0])
    print(len(gameweek_list))

    print("\nFixture List:")
    print(fixture_list[0])
    print(len(fixture_list))
