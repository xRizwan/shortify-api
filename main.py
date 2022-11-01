from fastapi import FastAPI
from db.database import engine
import db.models as models
from routes import users, urls

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(urls.router)
