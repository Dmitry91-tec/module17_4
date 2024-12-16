from app.backend.db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CreateTable


class User(Base):
    __tablename__ = 'users'                                            #имя таблице в БД
    __table_args__ = {'extend_existing': True}                         #удобно наследовать для вывода

    id = Column(Integer, primary_key=True, index=True)                 #уникальный идентификатор

    username = Column(String)                                          #название категории
    firstname = Column(String)                                         #название категории
    lastname = Column(String)                                          #название категории
    age = Column(Integer)                                              #название категории

    slug = Column(String, unique=True, index=True)                     #человекочитаемый URL

    tasks = relationship('Task', back_populates='user', cascade='save-update, merge, delete') #связь один ко многим


from sqlalchemy.schema import CreateTable
print(CreateTable(User.__table__))