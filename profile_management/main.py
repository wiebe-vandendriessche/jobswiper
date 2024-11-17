from fastapi import FastAPI
import database
import profiles

database.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.include_router(profiles.router)
