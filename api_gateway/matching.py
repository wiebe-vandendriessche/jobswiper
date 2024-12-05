import os
from fastapi import APIRouter


Profile_router = APIRouter(prefix="/profile", tags=["profiles"])

MATCHING_SERVICE_URL = os.getenv("MATCHING_MANAGEMENT_SERVICE_URL")
