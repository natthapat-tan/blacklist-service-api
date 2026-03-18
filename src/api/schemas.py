from pydantic import BaseModel

class BlacklistV1Request(BaseModel):
    id_number: str

class BlacklistV1Response(BaseModel):
    ref_id: str
    status: bool