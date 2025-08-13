from pydantic import BaseModel, EmailStr


class Module(BaseModel):
    moduleid: str
    name: str
    username: str
    msisdn: str
    pin: str
    password: str
    email: EmailStr
    is_active: bool
    base_url: str
    timeout: int
    max_retries: int
    second_wait: int
    provider: str


class ModulesConfig(BaseModel):
    modules: list[Module]
