from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database
from starlette import status
import auth
from auth import get_current_user
from typing import Annotated

models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()
app.include_router(auth.router)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@app.get("/", status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=404, detail="Authentication Failed")
    return {"User": user}
