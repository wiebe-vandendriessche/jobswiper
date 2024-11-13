from fastapi import Depends, FastAPI, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import requests
from validate import token, authenticate
import json

app = FastAPI()
security = HTTPBasic()


FLASK_SERVICE_URL = "http://flask_microservice:5000"  # Docker network alias


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI microservice!"}


@app.post("/login")
def login(auth: HTTPBasicCredentials = Depends(security)):
    if not auth:
        return None, ("missing credentials", 401)
    basicAuth = (auth.username, auth.password)
    token, err = authenticate(basicAuth)

    if not err:
        return token
    else:
        return err


@app.get("/test_auth")
def test_auth(request: Request):

    access, err = token(request)

    if err:
        return err

    access = json.loads(access)

    if access["admin"]:
        return "success!", 200
    else:
        return "not authorized", 401
