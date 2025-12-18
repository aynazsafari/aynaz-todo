from __future__ import annotations

from typing import Any, Dict, Optional

from motor.motor_asyncio import AsyncIOMotorDatabase


class TaskRepository:
    def __init__(self, db: AsyncIOMotorDatabase):
        self.col = db["tasks"]

    async def ensure_indexes(self) -> None:
        await self.col.create_index("id", unique=True)
        await self.col.create_index([("deleted_at", 1), ("status", 1), ("created_at", -1)])

    async def insert(self, doc: Dict[str, Any]) -> None:
        await self.col.insert_one(doc)

    async def get_by_id(self, task_id: str) -> Optional[Dict[str, Any]]:
        return await self.col.find_one({"id": task_id, "deleted_at": None}, {"_id": 0})

    async def update(self, task_id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        await self.col.update_one({"id": task_id, "deleted_at": None}, {"$set": patch})
        return await self.get_by_id(task_id)

    async def list(self, *, limit: int, offset: int, status: str | None, q: str | None) -> Dict[str, Any]:
        query: Dict[str, Any] = {"deleted_at": None}
        if status:
            query["status"] = status
        if q:
            query["title"] = {"$regex": q, "$options": "i"}

        total = await self.col.count_documents(query)
        cursor = self.col.find(query, {"_id": 0}).sort("created_at", -1).skip(offset).limit(limit)
        data = [doc async for doc in cursor]
        return {"data": data, "meta": {"pagination": {"limit": limit, "offset": offset, "total": total}}}
