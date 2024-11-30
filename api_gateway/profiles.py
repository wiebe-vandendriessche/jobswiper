from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from rest_interfaces.profile_interfaces import UserProfile
from main import verify_token_get_user


Profile_router = APIRouter(prefix="/profiles", tags=["profiles"])


# Route to create a user
@Profile_router.post("/profile")
async def profile(
    user: Annotated[dict, Depends(verify_token_get_user)], data: UserProfile
):
    return {"profile": user}
