from pydantic import BaseModel, EmailStr

# TODO Validasi FIELD


class ModuleConfig(BaseModel):
    model_config = {"from_attributes": True}


class ModuleInDB(ModuleConfig):
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


class ModuleListInDB(BaseModel):
    __root__: list[ModuleInDB]
