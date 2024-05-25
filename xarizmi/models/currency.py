from pydantic import BaseModel


class Currency(BaseModel):
    name: str

    def to_string(self) -> str:
        return self.name
