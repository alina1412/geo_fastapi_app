from pydantic import BaseModel


class FieldBase(BaseModel):
    id: int
    gfield: str

    class Config:
        orm_mode = True
