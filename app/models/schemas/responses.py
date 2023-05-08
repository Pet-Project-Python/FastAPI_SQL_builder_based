from pydantic import BaseModel


class SOkResponse(BaseModel):
    ok: bool
