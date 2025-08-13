from typing import Annotated

from fastapi import Depends, HTTPException, Request

from src.domain.member.rep_member import MemberRepository
from src.domain.module.rep_module import ModuleRepository
from src.service.auth.srv_dgproductauth import DigiposProductAuthService
from src.service.auth.srv_memberauth import MemberAuthService
from src.service.auth.srv_moduleauth import ModuleAuthService
from src.service.dto.srv_dtoservice import DataService, DigiposProductRepository


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


# DigiposProduct Dependency
def get_digipos_repo(
    data_service: DataService = Depends(get_data_service),
) -> DigiposProductRepository:
    return data_service.digipos_repo


DepDigiposRepo = Annotated[DigiposProductRepository, Depends(get_digipos_repo)]


# -------------------------------
# MemberAuthService Dependency
# -------------------------------
def get_member_auth_service(member_repo: DepMemberRepo) -> MemberAuthService:
    return MemberAuthService(member_repo)


DepMemberAuthService = Annotated[MemberAuthService, Depends(get_member_auth_service)]


# ModuleAuthService Dependency
def get_module_auth_service(module_repo: DepModuleRepo) -> ModuleAuthService:
    return ModuleAuthService(module_repo)


DepModuleAuthService = Annotated[ModuleAuthService, Depends(get_module_auth_service)]


# ProductAuthService Dependency
def get_digi_product_auth_service(
    digipos_repo: DepDigiposRepo,
) -> DigiposProductAuthService:
    return DigiposProductAuthService(digipos_repo)


DepDigiProductAuthService = Annotated[
    DigiposProductAuthService, Depends(get_digi_product_auth_service)
]
