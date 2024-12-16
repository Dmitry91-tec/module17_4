from fastapi import FastAPI
from app.backend.db import engine, Base
from app.routers import user, task  #подключаем файлы из роутера

app = FastAPI()                   #инициализация fastapi

app.include_router(user.router)    #подключаем внешние роутеры: user
app.include_router(task.router)    #подключаем внешние роутеры: task

Base.metadata.create_all(bind=engine)

@app.get("/")
async def welcome():
    return {"message":"Welcome to Taskmanager"}