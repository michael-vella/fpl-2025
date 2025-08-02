from typing import List

from fpl.repositories.player_type_repository import PlayerTypeRepository
from fpl.schemas import PlayerTypeResponse


class PlayerTypeService:
    def __init__(self, repository: PlayerTypeRepository):
        self._repository = repository
        self._types: List[PlayerTypeResponse] = self._repository.get_all() # load only once

    def get_id_by_name(self, name: str) -> int:
        for pt in self._types:
            if pt.singular_name_short.lower() == name.lower():
                return pt.id
        raise ValueError(f"Player type '{name}' not found")