from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, database


models.Base.metadata.create_all(bind=database.engine)


app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()
        

@app.get("/", status_code=200)
async def get_user(db: Session = Depends(get_db)):
    db_user = db.query(models.User).first()  # Example of querying a user
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"User": db_user}