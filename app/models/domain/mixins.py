from pydantic import BaseModel


class SUserId(BaseModel):
    user_id: int


class SId(BaseModel):
    id: int
