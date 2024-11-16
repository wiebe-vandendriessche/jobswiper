from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import httpx
from fastapi.security import OAuth2PasswordRequestForm
import os

app = FastAPI()

# Authentication service URL from environment variable
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL")
if not AUTH_SERVICE_URL:
    raise HTTPException(status_code=500, detail="AUTH_SERVICE_URL is not set in environment variables")

class CreateUserRequest(BaseModel):
    username: str
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str

#--------------------------------------------- CALLING /AUTH/  TO CREATE USER ---------------------------------------------

SIGNUP_AUTH_API_URL = f"{AUTH_SERVICE_URL}/auth/"    

# Function to create a user in the external authentication API
async def create_user_in_external_api(username: str, password: str):
    async with httpx.AsyncClient() as client:
        # Send a POST request to the external authentication API to create a user
        response = await client.post(
            SIGNUP_AUTH_API_URL,
            json={"username": username, "password": password}
        )

        if response.status_code == 201:
            return {"message": "User created successfully."}
        else:
            # Handle errors from the external API (e.g., username already exists)
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Failed to create user: {response.text}"
            )
            
# Route to create a user
@app.post("/sign-up")
async def create_user(credentials: CreateUserRequest):
    try:
        # Call the external API to create the user
        result = await create_user_in_external_api(credentials.username, credentials.password)
        return result
    except HTTPException as e:
        # If the external API fails, pass the error message
        raise e
    
    
#--------------------------------------------- CALLING /AUTH/TOKEN  TO RETRIEVE JWT TOKEN ---------------------------------------------
    
TOKEN_AUTH_API_URL = f"{AUTH_SERVICE_URL}/auth/token"  # The external API's token endpoint

@app.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
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
            raise HTTPException(status_code=400, detail=f"Request to external auth service failed: {e}")
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail=f"External auth service error: {e}")
    
    # Return the token and token type from the external service's response
    return TokenResponse(**auth_data)