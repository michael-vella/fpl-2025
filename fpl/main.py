from fpl.repositories import PlayerTypeRepository
from fpl.services import PlayerTypeService

if __name__ == "__main__":
    player_type_repo = PlayerTypeRepository()
    player_type_service = PlayerTypeService(player_type_repo)

    player_types = player_type_repo.get_all()
    print(f"Player Types: {player_types}")

    def_id = player_type_service.get_id_by_name("def")
    print(f"Defender ID: {def_id}")
