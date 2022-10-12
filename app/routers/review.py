from typing import List, Union
from fastapi import APIRouter, HTTPException, Depends

from app.models.review import ReviewBaseDB, ReviewFullDB
from app.core.review import reviewCore
from app.models.message_db import MessageDB

review_router = APIRouter()


@review_router.get('/reviews', name='List reviews', tags=['Wines review'], response_model=List[ReviewFullDB])
async def get_reviews(skip: int = 0, limit: Union[int, None] = None):
    try:
        return reviewCore.get_all()
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.post('/review', name='Create a review', tags=['Wines review'], response_model=MessageDB)
async def get(data:ReviewBaseDB):
    try:
        return reviewCore.save_one(data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.get('/review/{pid}', name='Get a review', tags=['Wines review'], response_model=ReviewFullDB)
async def get_review(pid: str):
    try:
        return reviewCore.get_one(pid)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.patch('/review/{pid}', name='Update a review', tags=['Wines review'], response_model=MessageDB)
async def update_review(pid: str, data: ReviewBaseDB):
    try:
        return reviewCore.update_one(pid, data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.delete('/review/{pid}', name='Delete a review', tags=['Wines review'])
async def delete_review(pid: str):
    try:
        return reviewCore.delete_one(pid)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
