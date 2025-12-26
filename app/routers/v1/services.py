from fastapi import APIRouter, Depends

from app.core.dependencies import require_permission, get_current_user

from app.models.user import User

router = APIRouter(prefix="/services", tags=["services"])


@router.get("/manager_notes", dependencies=[Depends(require_permission("notes", "read"))])
async def get_notes(
     current_user: User = Depends(get_current_user)
):
    return {
        "READ MANAGER NOTES": "YES"
    }


@router.put("/manager_notes", dependencies=[Depends(require_permission("notes", "write"))])
async def update_notes(
     current_user: User = Depends(get_current_user)
):
    return {
        "WRITE MANAGER NOTES": "YES"
    }


@router.get("/admin_photos", dependencies=[Depends(require_permission("photos", "read"))])
async def get_notes(
     current_user: User = Depends(get_current_user)
):
    return {
        "GET ADMIN PHOTOS": "YES"
    }