from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import update, delete
from src.config.database import get_db
from src.model.models import Task
from src.schema.task import TaskCreate, TaskOut
from src.core.security import get_current_user
from typing import List

router = APIRouter()

@router.post("/", response_model=TaskOut)
async def create_task(task: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    new_task = Task(**task.dict(), user_id=current_user.id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

@router.get("/", response_model=List[TaskOut])
async def get_tasks(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Task).where(Task.user_id == current_user.id).offset(skip).limit(limit))
    return result.scalars().all()

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task_db = result.scalar_one_or_none()
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(task_db, key, value)
    await db.commit()
    await db.refresh(task_db)
    return task_db

@router.delete("/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == current_user.id))
    task_db = result.scalar_one_or_none()
    if not task_db:
        raise HTTPException(status_code=404, detail="Task not found")
    await db.delete(task_db)
    await db.commit()
    return {"detail": "Task deleted successfully"}

