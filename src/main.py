from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import auth, tasks
import uvicorn
from src.config.database import engine
from src.model import models

app = FastAPI()


app.include_router(auth.router, tags=["Auth"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])



# Don't use: models.Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
