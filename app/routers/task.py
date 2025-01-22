from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from app.backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated

from app.models import *
from app.schemas import CreateTask, UpdateTask

from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(
        db: Annotated[Session, Depends(get_db)],
        task_id: int
):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        return task
    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} was not found"
    )


@router.post('/create')
async def creat_tasks(db: Annotated[Session, Depends(get_db)], user_id, create_task: CreateTask):
    # Дополнительно принимает модель CreateTask и user_id.

    user = db.scalar(select(User).where(User.id == user_id))
    if user is not None:
        db.execute(
            insert(Task).values(
                title=create_task.title,
                content=create_task.content,
                priority=create_task.priority,
                user_id=user_id,
                slug=slugify(create_task.title)
            )
        )

        db.commit()
        return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}

    raise HTTPException(
        status_code=404,
        detail=f"User {user_id} was not found"
    )


@router.put('/update')
async def update_tasks(
        db: Annotated[Session, Depends(get_db)],
        task_id: int,
        task_update_model: UpdateTask
):
    task = db.scalar(select(Task).where(Task.id == task_id))

    if task is not None:
        db.execute(
            update(Task).where(Task.id == task_id).values(
                title=task_update_model.title,
                content=task_update_model.content,
                priority=task_update_model.priority,
            )
        )

        db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': f'Task {task.title} update is successful!'
        }

    raise HTTPException(
        status_code=404,
        detail=f"Task {task_id} was not found"
    )


@router.delete('/delete')
async def delete_tasks(
        db: Annotated[Session, Depends(get_db)],
        task_id: int,
):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is not None:
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()

        return {
            'status_code': status.HTTP_200_OK,
            'transaction': f'Task {task.title} delete is successful!'
        }

    raise HTTPException(
        status_code=404,
        detail=f'Task {task_id} was not found'
    )

