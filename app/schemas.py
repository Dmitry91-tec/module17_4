from pydantic import BaseModel

class CreateUser(BaseModel):
    username: str
    firstname: str
    lastname: int
    age: int

class UpdateUser(BaseModel):
    firstname: str
    lastname: int
    age: int

class CreateTask(BaseModel):
    title: str
    content: str
    priority: int

class UpdateTask(BaseModel):
    title: str
    content: int
    priority: int

class Config:
    orm_mode = True