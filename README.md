# fpl-2025
Repository to scrape and analyse Fantasy Premier League (FPL) 2025 and use this data to take decisions.

## To run tests:

1. Run `.venv\Scripts\activate` to activate virtual environment.
2. Run `pip install -e .` to install the `fpl` package.
3. Run `python tests/runtests.py` to run all of the tests.

## To-do:

- ~~Create tests for `data_parser.py`.~~
- ~~Implement player type service to get player types.~~
- ~~Refactor tests and find better way to run integration/unit tests separately.~~
- Implement gameweek processor that retrieves the id of the next fixture. Gameweek service should be stateless and there is no need to keep the list of gameweeks as state to the constructor.
- Refactor player type service to player type processor that is also stateless.
- Implement player services (most probably best to implement one per each player type).
- As part of player service, implement linear regression model that based on player cost, determine other player statistics.
- Implement gameweek, fixture and team services.

# To refactor:

- Refactor repositories to remove code deduplication. Have two repositories only. One `BootstrapRepository` to get the data from the `bootstrap-static/` endpoint and another one to get the data from the `fixtures/` endpoint.