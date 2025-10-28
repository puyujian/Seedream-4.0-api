from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from ..config import Settings, get_settings
from ..schemas import TaskStatusResponse, HistoryListResponse
from ..utils.task_store import TaskStore

router = APIRouter(prefix="/tasks", tags=["tasks"])

_store: Optional[TaskStore] = None


def get_task_store(settings: Settings = Depends(get_settings)) -> TaskStore:
    global _store
    if _store is None:
        _store = TaskStore(
            history_file=Path(settings.HISTORY_FILE),
            max_history_size=settings.MAX_HISTORY_SIZE,
        )
    return _store


@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str, store: TaskStore = Depends(get_task_store)):
    task = await store.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskStatusResponse(
        task_id=task.id,
        status=task.status,
        progress=task.progress,
        images=task.images,
        error=task.error,
        created_at=task.created_at,
        completed_at=task.completed_at,
    )


@router.get("/", response_model=list[TaskStatusResponse])
async def list_tasks(store: TaskStore = Depends(get_task_store)):
    tasks = await store.list_tasks()
    return [
        TaskStatusResponse(
            task_id=task.id,
            status=task.status,
            progress=task.progress,
            images=task.images,
            error=task.error,
            created_at=task.created_at,
            completed_at=task.completed_at,
        )
        for task in tasks
    ]


@router.get("/history", response_model=HistoryListResponse)
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    store: TaskStore = Depends(get_task_store),
):
    total, items = await store.list_history(page=page, page_size=page_size)
    return HistoryListResponse(
        total=total,
        items=items,
        page=page,
        page_size=page_size,
    )
