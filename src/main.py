from fastapi import FastAPI
from src.model import models
from src.config.database import engine
from src.routes import auth, tasks

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth.router)
app.include_router(tasks.router, prefix="/tasks")