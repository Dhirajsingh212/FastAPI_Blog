from fastapi import FastAPI
from routers import users, auth, blogs
from db import models
from db.database import engine


app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(blogs.router)


@app.get("/")
def get_work():
    return "working"
