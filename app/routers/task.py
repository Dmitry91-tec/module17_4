from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated

from app.models import *
from sqlalchemy import insert
from app.schemas import UpdateTask, CreateTask

from slugify import slugify
from sqlalchemy import select
from sqlalchemy import update

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/all_tasks")
async def get_all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    if tasks is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There are no task'
        )
    return tasks

@router.get("/tasks_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_slug: str):
    task = db.scalar(select(Task).where(Task.slug == task_slug))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task not found'
        )
    task_id = db.scalars(select(Task).where(Task.user_id))

    return task_id

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask):
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   #user_id=create_task.user,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_slug: str, update_task: UpdateTask):
    task = db.scalar(select(Task).where(Task.slug == task_slug))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )

    db.execute(update(Task).where(Task.slug == task_slug)
               .values(title=update_task.title,
                       content=update_task.content,
                       priority=update_task.priority))
                       #completed=update_task.completed,
                       #user_id=update_task.user,
                       #slug=slugify(update_task.title)))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task update is successful'
    }

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no task found'
        )
    db.execute(update(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Task delete is successful'
    }
