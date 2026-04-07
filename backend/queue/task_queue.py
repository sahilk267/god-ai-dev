"""Task queue management for multiple projects"""

import asyncio
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import json
from backend.core.logger import get_logger

logger = get_logger(__name__)

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    prompt: str
    status: TaskStatus
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result: Optional[Dict] = None
    error: Optional[str] = None

class TaskQueue:
    def __init__(self, max_concurrent: int = 3):
        self.tasks: Dict[str, Task] = {}
        self.queue: asyncio.Queue = asyncio.Queue()
        self.max_concurrent = max_concurrent
        self.current_running = 0
        self._running_lock = asyncio.Lock()
        self._workers = []
    
    async def add_task(self, prompt: str) -> str:
        import uuid
        task_id = str(uuid.uuid4())
        
        task = Task(
            id=task_id,
            prompt=prompt,
            status=TaskStatus.PENDING,
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        await self.queue.put(task_id)
        logger.info(f"Task {task_id} added to queue")
        
        return task_id
    
    async def start_workers(self, orchestrator):
        for i in range(self.max_concurrent):
            worker = asyncio.create_task(self._worker_loop(orchestrator, i))
            self._workers.append(worker)
        logger.info(f"Started {self.max_concurrent} workers")
    
    async def _worker_loop(self, orchestrator, worker_id: int):
        while True:
            try:
                task_id = await self.queue.get()
                
                if task_id not in self.tasks:
                    continue
                
                task = self.tasks[task_id]
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()
                async with self._running_lock:
                    self.current_running += 1
                
                logger.info(f"Worker {worker_id} processing task {task_id}")
                
                try:
                    result = await orchestrator.run_god_mode(task.prompt, task_id)
                    task.status = TaskStatus.COMPLETED
                    task.result = result
                except Exception as e:
                    task.status = TaskStatus.FAILED
                    task.error = str(e)
                    logger.error(f"Task {task_id} failed: {e}")
                
                task.completed_at = datetime.now()
                async with self._running_lock:
                    self.current_running -= 1
                self.queue.task_done()
                
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Worker {worker_id} error: {e}")
    
    async def get_task_status(self, task_id: str) -> Optional[Dict]:
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        return {
            "id": task.id,
            "status": task.status.value,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "result": task.result,
            "error": task.error
        }
    
    async def cancel_task(self, task_id: str) -> bool:
        if task_id not in self.tasks:
            return False
        
        task = self.tasks[task_id]
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        
        return False

task_queue = TaskQueue()