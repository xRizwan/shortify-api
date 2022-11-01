from fastapi import FastAPI
from db import models
from db.database import engine
from routes import users, urls

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(urls.router)
