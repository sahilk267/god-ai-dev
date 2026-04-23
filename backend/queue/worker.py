"""Background worker for async task processing"""

import asyncio
from typing import Optional
from backend.core.logger import get_logger
from .task_queue import task_queue

logger = get_logger(__name__)

class BackgroundWorker:
    def __init__(self):
        self.is_running = False
    
    async def start(self, orchestrator):
        self.is_running = True
        await task_queue.start_workers(orchestrator)
        logger.info("Background worker started")
    
    async def stop(self):
        self.is_running = False
        # Cancel all actual worker tasks in the queue
        for worker_task in task_queue._workers:
            worker_task.cancel()
        # Wait for all workers to finish
        if task_queue._workers:
            await asyncio.gather(*task_queue._workers, return_exceptions=True)
            task_queue._workers.clear()
        logger.info("Background worker stopped")

background_worker = BackgroundWorker()