from typing import Annotated

from fastapi import Depends, HTTPException, Request

from src.domain.member.rep_member import MemberRepository


# dependency buat ngambil data_service
def get_data_service(request: Request):
    ds = getattr(request.app.state, "data_service", None)
    if ds is None:
        raise HTTPException(status_code=503, detail="DataService not ready")
    return ds


# dependency buat member_repo
def get_member_repo(data_service=Depends(get_data_service)):
    return data_service.member_repo


# dependency buat module_repo (nanti kalau udah siap)
def get_module_repo(data_service=Depends(get_data_service)):
    return data_service.module_repo


DepMemberRepo = Annotated[
    MemberRepository,
    Depends(get_member_repo),
]
