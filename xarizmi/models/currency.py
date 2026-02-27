from dataclasses import dataclass


@dataclass
class Currency:
    name: str

    def to_string(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Currency):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)
