import json
from fastapi import FastAPI, HTTPException, Depends, APIRouter
import httpx
import redis
from typing import Annotated
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from caching import cache_token, get_user_from_cached_token

import os


app = FastAPI()
# redis caching database init:


# Authentication service URL from environment variable
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
if not AUTH_SERVICE_URL:
    raise HTTPException(
        status_code=500, detail="AUTH_SERVICE_URL is not set in environment variables"
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class CreateUserRequest(BaseModel):
    username: str
    password: str


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="login")


# Updated get_current_user to delegate JWT verification to AuthService
async def verify_token_get_user(token: str = Depends(oauth2_bearer)):
    async with httpx.AsyncClient() as client:
        """
        the token is retrieved from each bearer in the protected resources.
        the token is then sent to the AuthService for verification.
        the user information is then parsed from the AuthService
        and returned to the protected route.
        """
        try:
            # check if in cache
            user = get_user_from_cached_token(token)
            if user:
                return json.loads(user)
            else:  # Send the token to the AuthService for verification
                response = await client.post(
                    f"{AUTH_SERVICE_URL}/auth/verify-token",
                    headers={"Authorization": f"Bearer {token}"},
                )
                response.raise_for_status()  # Raise error for invalid token
                # Parse the user information from AuthService response
                print(response.text)
                cache_token(token, response.text)
                return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=400, detail=f"Request to AuthService failed: {e}"
            )
        except httpx.HTTPStatusError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=501, detail=f"verifytoken failed: {e}")


# --------------------------------------------- CALLING /AUTH/  TO CREATE USER ---------------------------------------------

SIGNUP_AUTH_API_URL = f"{AUTH_SERVICE_URL}/auth/"


# Function to create a user in the external authentication API
async def create_user_in_auth_service(username: str, password: str):
    async with httpx.AsyncClient() as client:
        # Send a POST request to the external authentication API to create a user
        response = await client.post(
            SIGNUP_AUTH_API_URL, json={"username": username, "password": password}
        )

        if response.status_code == 201:
            return {"message": "User created successfully."}
        else:
            # Handle errors from the external API (e.g., username already exists)
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to create user: {response.text}",
            )


@app.post("/sign-up")
async def create_user(credentials: CreateUserRequest):
    """
    User Creation Endpoint (/sign-up):

    This route calls an external authentication API to create a user. It sends a POST request to the /auth/ endpoint of the authentication service with the username and password.
    It handles both success and failure cases from the external API.

    It then creates a profile in the database based on the arguments/preferences given.

    """
    try:
        # Call the external API to create the user
        result = await create_user_in_auth_service(
            credentials.username, credentials.password
        )

        return result
    except HTTPException as e:
        # If the external API fails, pass the error message
        raise e


# --------------------------------------------- CALLING /AUTH/TOKEN  TO RETRIEVE JWT TOKEN ---------------------------------------------

TOKEN_AUTH_API_URL = (
    f"{AUTH_SERVICE_URL}/auth/token"  # The external API's token endpoint
)


@app.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login Endpoint (/login):

    This route facilitates user login by sending a POST request to the external authentication API's /auth/token endpoint.
    It uses the OAuth2PasswordRequestForm to extract the username and password from the form data sent by the user.
    It retrieves the token from the external service, which is then returned to the client.
    """
    # Prepare the data to send to the external auth service (form data)
    data = {
        "username": form_data.username,
        "password": form_data.password,
        "grant_type": "password",  # Include any other required fields by the external service
    }

    async with httpx.AsyncClient() as client:
        # Make the POST request to the external auth service
        try:
            response = await client.post(TOKEN_AUTH_API_URL, data=data)
            response.raise_for_status()  # Will raise an exception for 4xx/5xx status codes
            auth_data = response.json()  # Parse the JSON response
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=400, detail=f"Request to external auth service failed: {e}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"External auth service error: {e}",
            )

    # Return the token and token type from the external service's response
    return TokenResponse(**auth_data)


# --------------------------------------------- PROTECTED ROUTES (Authentication Required) ---------------------------------------------

"""
These routes require a valid token to access.
The verify_token_get_user function is used to decode and validate the JWT token.
If the token is valid, it returns the username and user ID, which are used in the protected routes.
If the token is invalid or expired, the user receives a 401 Unauthorized response.
"""


@app.get("/protected-endpoint")
async def protected_data(user: Annotated[dict, Depends(verify_token_get_user)]):
    # This route is now protected. It can only be accessed by users with a valid token.
    return {"message": f"Hello {user['username']}, you have access!"}


# -------------------------------------------------Profile Management Service --------------------------------------------------------------------------
from profiles import Profile_router

app.include_router(Profile_router)

# ------------------------------------------------- Job Management Service -----------------------------------------------------------------------------

from jobs import Jobs_router

app.include_router(Jobs_router)
