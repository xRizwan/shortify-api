from fastapi import FastAPI
from db import models
from db.database import engine
from routes import users, urls
import uvicorn

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(urls.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
