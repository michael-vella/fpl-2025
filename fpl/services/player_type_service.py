from typing import List

from fpl.schemas import PlayerTypeResponse


class PlayerTypeService:
    def __init__(self, player_types: List[PlayerTypeResponse]):
        self._types = player_types

    def get_id_by_name(self, name: str) -> int:
        for pt in self._types:
            if pt.singular_name.lower() == name.lower():
                return pt.id
        raise ValueError(f"Player type '{name}' not found")