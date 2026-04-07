"""Background worker for async task processing"""

import asyncio
from typing import Optional
from backend.core.logger import get_logger
from .task_queue import task_queue

logger = get_logger(__name__)

class BackgroundWorker:
    def __init__(self):
        self.is_running = False
        self._task = None
    
    async def start(self, orchestrator):
        self.is_running = True
        await task_queue.start_workers(orchestrator)
        logger.info("Background worker started")
    
    async def stop(self):
        self.is_running = False
        if self._task:
            self._task.cancel()
        logger.info("Background worker stopped")

background_worker = BackgroundWorker()