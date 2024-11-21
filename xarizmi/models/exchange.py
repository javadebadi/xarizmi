from pydantic import BaseModel


class Exchange(BaseModel):
    name: str

    def to_string(self) -> str:
        return self.name
