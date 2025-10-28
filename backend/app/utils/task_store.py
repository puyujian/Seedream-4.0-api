from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
from uuid import uuid4
from asyncio import Lock

from ..schemas import TaskStatus, GenerationHistory


@dataclass
class TaskRecord:
    """In-memory representation of a generation task"""

    id: str
    type: str
    status: TaskStatus
    prompt: str
    negative_prompt: Optional[str]
    parameters: Dict[str, Any]
    images: List[str]
    progress: Optional[int]
    error: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["created_at"] = self.created_at.isoformat()
        data["completed_at"] = self.completed_at.isoformat() if self.completed_at else None
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TaskRecord":
        return cls(
            id=data["id"],
            type=data["type"],
            status=TaskStatus(data["status"]),
            prompt=data.get("prompt", ""),
            negative_prompt=data.get("negative_prompt"),
            parameters=data.get("parameters", {}),
            images=data.get("images", []),
            progress=data.get("progress"),
            error=data.get("error"),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
        )


class TaskStore:
    """Simple task and history store based on JSON persistence"""

    def __init__(self, history_file: Path, max_history_size: int = 1000) -> None:
        self.history_file = history_file
        self.max_history_size = max_history_size
        self._tasks: Dict[str, TaskRecord] = {}
        self._history: Dict[str, GenerationHistory] = {}
        self._lock = Lock()
        self._load_history()

    def _load_history(self) -> None:
        if not self.history_file.exists():
            self.history_file.parent.mkdir(parents=True, exist_ok=True)
            self.history_file.write_text(json.dumps({"items": []}, ensure_ascii=False, indent=2), encoding="utf-8")

        try:
            data = json.loads(self.history_file.read_text(encoding="utf-8"))
            items = data.get("items", [])
            for item in items:
                history = GenerationHistory(**item)
                self._history[history.task_id] = history
                task = TaskRecord(
                    id=history.task_id,
                    type=history.type,
                    status=TaskStatus.COMPLETED,
                    prompt=history.prompt,
                    negative_prompt=history.negative_prompt,
                    parameters=history.parameters,
                    images=history.images,
                    progress=100,
                    error=None,
                    created_at=history.created_at,
                    completed_at=history.created_at,
                )
                self._tasks[task.id] = task
        except json.JSONDecodeError:
            self._tasks = {}
            self._history = {}

    async def create_task(
        self,
        task_type: str,
        prompt: str,
        negative_prompt: Optional[str],
        parameters: Dict[str, Any],
    ) -> TaskRecord:
        async with self._lock:
            task_id = str(uuid4())
            now = datetime.utcnow()
            task = TaskRecord(
                id=task_id,
                type=task_type,
                status=TaskStatus.PENDING,
                prompt=prompt,
                negative_prompt=negative_prompt,
                parameters=parameters,
                images=[],
                progress=0,
                error=None,
                created_at=now,
                completed_at=None,
            )
            self._tasks[task_id] = task
            return task

    async def update_task(
        self,
        task_id: str,
        *,
        status: Optional[TaskStatus] = None,
        progress: Optional[int] = None,
        images: Optional[List[str]] = None,
        error: Optional[str] = None,
        completed: bool = False,
    ) -> Optional[TaskRecord]:
        async with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None

            if status:
                task.status = status
            if progress is not None:
                task.progress = progress
            if images is not None:
                task.images = images
            if error is not None:
                task.error = error
            if completed:
                task.completed_at = datetime.utcnow()

            self._tasks[task_id] = task

            if completed and task.status == TaskStatus.COMPLETED:
                await self._persist_history(task)
            return task

    async def fail_task(self, task_id: str, error: str) -> Optional[TaskRecord]:
        return await self.update_task(
            task_id,
            status=TaskStatus.FAILED,
            progress=100,
            error=error,
            completed=True,
        )

    async def complete_task(self, task_id: str, images: List[str]) -> Optional[TaskRecord]:
        return await self.update_task(
            task_id,
            status=TaskStatus.COMPLETED,
            progress=100,
            images=images,
            completed=True,
        )

    async def set_processing(self, task_id: str) -> Optional[TaskRecord]:
        return await self.update_task(task_id, status=TaskStatus.PROCESSING, progress=10)

    async def get_task(self, task_id: str) -> Optional[TaskRecord]:
        async with self._lock:
            return self._tasks.get(task_id)

    async def list_tasks(self) -> List[TaskRecord]:
        async with self._lock:
            return sorted(self._tasks.values(), key=lambda t: t.created_at, reverse=True)

    async def list_history(self, page: int = 1, page_size: int = 20) -> tuple[int, List[GenerationHistory]]:
        async with self._lock:
            items = sorted(self._history.values(), key=lambda h: h.created_at, reverse=True)
            total = len(items)
            start = (page - 1) * page_size
            end = start + page_size
            return total, items[start:end]

    async def toggle_favorite(self, task_id: str, favorite: bool) -> Optional[GenerationHistory]:
        async with self._lock:
            history = self._history.get(task_id)
            if not history:
                return None
            history.favorite = favorite
            self._history[task_id] = history
            await self._dump_history()
            return history

    async def _persist_history(self, task: TaskRecord) -> None:
        history = GenerationHistory(
            id=str(uuid4()),
            task_id=task.id,
            type=task.type,
            prompt=task.prompt,
            negative_prompt=task.negative_prompt,
            parameters=task.parameters,
            images=task.images,
            created_at=task.completed_at or datetime.utcnow(),
            favorite=False,
        )
        self._history[task.id] = history

        # Trim history if exceeds max size
        if len(self._history) > self.max_history_size:
            # remove oldest entries
            sorted_items = sorted(self._history.items(), key=lambda kv: kv[1].created_at)
            to_remove = len(self._history) - self.max_history_size
            for key, _ in sorted_items[:to_remove]:
                self._history.pop(key, None)

        await self._dump_history()

    async def _dump_history(self) -> None:
        data = {
            "items": [history.model_dump(mode="json") for history in self._history.values()]
        }
        self.history_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
