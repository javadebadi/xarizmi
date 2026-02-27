from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class Exchange:
    name: str

    def to_string(self) -> str:
        return self.name

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Exchange):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)


class ExchangeList(BaseModel):
    items: list[Exchange]
