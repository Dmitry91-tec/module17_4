from app.backend.db import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = 'tasks'                                                         #имя таблице в БД
    __table_args__ = {'extend_existing': True}                                      #удобно наследовать для вывода

    id = Column(Integer, primary_key=True, index=True)                              #уникальный идентификатор

    title = Column(String)                                                          #название категории
    content = Column(String)                                                        #название категории
    priority = Column(Integer, default=0)                                           #название категории
    completed = Column(Boolean, default=False)                                      #название категории
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True, index=True)    #связь с task
    slug = Column(String, unique=True, index=True)

    user = relationship('User', back_populates='tasks')                    #связь многие к одному


from sqlalchemy.schema import CreateTable
print(CreateTable(Task.__table__))