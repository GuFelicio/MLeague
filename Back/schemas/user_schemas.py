from pydantic import BaseModel

class LoginSchema(BaseModel):
    username: str
    password: str

class PUUIDSchema(BaseModel):
    puuid: str
