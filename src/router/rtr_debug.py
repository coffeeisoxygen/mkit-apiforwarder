from fastapi import APIRouter

from src.dependencies.dep_data import DepMemberRepo, DepModuleRepo

router = APIRouter()


@router.get("/debug")
async def debug_all(member_repo: DepMemberRepo, module_repo: DepModuleRepo):
    """Show all members and modules for debugging."""
    members = [m.model_dump() for m in member_repo.get_all_members()]
    modules = [m.model_dump() for m in module_repo.get_all_modules()]
    return {"members": members, "modules": modules}


@router.get("/debug/member/{member_id}")
async def debug_member(member_id: str, member_repo: DepMemberRepo):
    """Show member details by ID for debugging."""
    member = member_repo.get_member_by_id(member_id)
    if not member:
        return {"error": "Member not found"}
    return member.model_dump()


@router.get("/debug/module/{module_id}")
async def debug_module(module_id: str, module_repo: DepModuleRepo):
    """Show module details by ID for debugging."""
    module = module_repo.get_module_by_id(module_id)
    if not module:
        return {"error": "Module not found"}
    return module.model_dump()
