import os
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
import auth
from typing import Annotated

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.include_router(auth.router)
