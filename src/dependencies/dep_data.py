from typing import Annotated

from fastapi import Depends, HTTPException, Request

from src.domain.member.rep_member import MemberRepository
from src.domain.module.rep_module import ModuleRepository
from src.service.srv_dtoservice import DataService
from src.service.srv_memberauth import MemberAuthService


# dependency buat ngambil data_service
def get_data_service(request: Request):
    """Get the data service instance from the request.

    This dependency retrieves the DataService instance from the FastAPI application state.

    Args:
        request (Request): The FastAPI request object.

    Raises:
        HTTPException: If the DataService is not ready.

    Returns:
        DataService: The DataService instance.
    """
    ds = getattr(request.app.state, "data_service", None)
    if ds is None:
        raise HTTPException(status_code=503, detail="DataService not ready")
    return ds


# dependency buat member_repo
def get_member_repo(data_service: DataService = Depends(get_data_service)):
    """Get the member repository.

    This dependency provides the member repository from the data service.

    Args:
        data_service (DataService, optional): The data service instance. Defaults to Depends(get_data_service).

    Returns:
        MemberRepository: The member repository.
    """
    return data_service.member_repo


DepMemberRepo = Annotated[
    MemberRepository,
    Depends(get_member_repo),
]


# dependency buat module_repo (nanti kalau udah siap)
def get_module_repo(data_service: DataService = Depends(get_data_service)):
    """Get the module repository.

    This dependency provides the module repository from the data service.

    Args:
        data_service (DataService, optional): The data service instance. Defaults to Depends(get_data_service).

    Returns:
        ModuleRepository: The module repository.

    """
    return data_service.module_repo


DepModuleRepo = Annotated[
    ModuleRepository,
    Depends(get_module_repo),
]


def get_member_auth_service(member_repo: DepMemberRepo = Depends()):
    """Dependency untuk MemberAuthService."""
    return MemberAuthService(member_repo)


DepMemberAuthService = Annotated[
    MemberAuthService,
    Depends(get_member_auth_service),
]
