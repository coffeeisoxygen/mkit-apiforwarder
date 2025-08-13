from typing import Annotated

from fastapi import Depends, HTTPException, Request

from src.domain.member.rep_member import MemberRepository
from src.domain.module.rep_module import ModuleRepository
from src.service.srv_dtoservice import DataService
from src.service.srv_memberauth import MemberAuthService
from src.service.srv_moduleauth import ModuleAuthService


# -------------------------------
# DataService Dependency
# -------------------------------
def get_data_service(request: Request) -> DataService:
    ds = getattr(request.app.state, "data_service", None)
    if ds is None:
        raise HTTPException(status_code=503, detail="DataService not ready")
    return ds


DepDataService = Annotated[DataService, Depends(get_data_service)]


# -------------------------------
# MemberRepository Dependency
# -------------------------------
def get_member_repo(
    data_service: DataService = Depends(get_data_service),
) -> MemberRepository:
    return data_service.member_repo


DepMemberRepo = Annotated[MemberRepository, Depends(get_member_repo)]


# -------------------------------
# ModuleRepository Dependency
# -------------------------------
def get_module_repo(
    data_service: DataService = Depends(get_data_service),
) -> ModuleRepository:
    return data_service.module_repo


DepModuleRepo = Annotated[ModuleRepository, Depends(get_module_repo)]


# -------------------------------
# MemberAuthService Dependency
# -------------------------------
def get_member_auth_service(member_repo: DepMemberRepo) -> MemberAuthService:
    return MemberAuthService(member_repo)


# ModuleAuthService Dependency
def get_module_auth_service(module_repo: DepModuleRepo) -> ModuleAuthService:
    return ModuleAuthService(module_repo)
