from pydantic import BaseModel

class BlacklistV1Request(BaseModel):
    id: str

class BlacklistV1Response(BaseModel):
    ref_id: str
    provider: list
    status: bool