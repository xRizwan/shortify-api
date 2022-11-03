from fastapi import FastAPI
from db import models
from db.database import engine
from routes import users, urls
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

origins = ['https://.*\.vercel\.app', "http://localhost:5173", "*", ]

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(users.router)
app.include_router(urls.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
