from fastapi import FastAPI
import requests

app = FastAPI()

FLASK_SERVICE_URL = "http://flask_microservice:5000"  # Docker network alias

@app.get('/')
def read_root():
    return {"message": "Hello from FastAPI microservice!"}

@app.get('/call_flask')
def call_flask_microservice():
    response = requests.get(f"{FLASK_SERVICE_URL}/")
    return {"message": f"Response from Flask microservice: {response.json()['message']}"}