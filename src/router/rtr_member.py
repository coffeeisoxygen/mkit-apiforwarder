from fastapi import APIRouter

from src.dependencies.dep_data import DepMemberRepo

router = APIRouter()


@router.get("/members")
async def list_members(member_repo: DepMemberRepo):
    """Endpoint untuk nampilin semua member.

    Pake dependency injection ke MemberRepository.
    """
    members = member_repo.get_all_members()
    # Convert semua Pydantic object ke dict
    return [m.dict() for m in members]


@router.get("/members/{memberid}")
async def get_member(memberid: str, member_repo: DepMemberRepo):
    """Endpoint untuk ambil member by ID."""
    member = member_repo.get_member_by_id(memberid)
    if not member:
        return {"error": "Member not found"}
    return member.dict()
