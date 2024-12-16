from fastapi import APIRouter, Depends, status, HTTPException #роутер, связи, статусы состояния, ошибки
from sqlalchemy.orm import Session                            #Сессия БД
from app.backend.db_depends import get_db                     #Функция подключения к БД
from typing import Annotated                                  #Аннотации, Модели БД и Pydantic.
from app.models import User                                       #подключаем из моделей пользователей и task
from sqlalchemy import insert, select, update, delete
from app.schemas import CreateUser, UpdateUser                #подключаем категории создания и удаления пользователей

from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])            #сущность, работающая через префикс

@router.post('/create')
async def create_user(
        db: Annotated[Session, Depends(get_db)],
        user_create_model: CreateUser,
):
    db.execute(insert(User).values(username=user_create_model.username,
                                   firstname=user_create_model.firstname,
                                   lastname=user_create_model.lastname,
                                   age=user_create_model.age,
                                   slug=slugify(user_create_model.username)))
    db.commit()

    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
    }

'''@router.post("/create")                                      #декоратор подключим к нашему роутеру
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser): #создаем user согласно CreateUser shemas
    db.execute(insert(User).values(username=create_user.username,                        #подставляем в таблицу User
                                   firstname=create_user.firstname,                      #подставляем в таблицу User
                                   lastname=create_user.lastname,                        #подставляем в таблицу User
                                   age=create_user.age,                                  #подставляем в таблицу User
                                   slug=slugify(create_user.username)))                  #значение формируем из библиотеки slugify
    db.commit()                                                                          #сохраняем изменения в БД
    return {
        'status_code': status.HTTP_201_CREATED,                                          #статус,что все в порядке
        'transaction': 'Successful'
    }'''
#-----------------------------------------------
@router.get("/user_id")                                                            #декоратор подключим к нашему роутеру
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))                       #поиск user с таким id
    if user is not None:                                                       #если такого значения нет, то вывести ошибку
        return user

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='There is no user found'
    )

#---------------------------------
@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users

#-----------------------------

@router.put("/update")                                                     #декоратор подключим к нашему роутеру
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, update_user: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))               #поиск user с таким id
    if user is None:                                                       #если такого значения нет, то вывести ошибку
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no user found'
        )

    db.execute(update(User).where(User.id == user_id).values(              #внести изменения в БД
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age))

    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User update is successful'
    }
#-----------------------------------------------


@router.delete("/delete")                          #декоратор подключим к нашему роутеру
async def delete_user(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='There is no category found'
        )
    db.execute(delete(User).where(User.id == user_id))
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }