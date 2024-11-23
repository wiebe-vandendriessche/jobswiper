from fastapi import FastAPI
import database
import jobs

database.Base.metadata.create_all(bind=database.engine)
app = FastAPI()
app.include_router(jobs.router)