from typing import List, Optional
from fastapi import APIRouter, HTTPException

from app.models.review import ReviewBaseDB, ReviewFullDB
from app.core.review import reviewCore
from app.models.message_db import MessageDB
from starlette.responses import JSONResponse

review_router = APIRouter()


@review_router.get('/reviews', name='List reviews', tags=['Wines review'], response_model=List[ReviewFullDB])
async def get_reviews(limit: Optional[int] = 20, offset: Optional[int] = 1):
    if limit < 0:
        return JSONResponse(content={
            "detail": "limit must be positive integer"
        }, status_code=422)
    if offset <= 0:
        return JSONResponse(content={
            "detail": "offset must be positive integer"
        }, status_code=422)
    try:
        return reviewCore.get_all(limit, offset)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.post('/reviews', name='Create a review', tags=['Wines review'], response_model=MessageDB)
async def get(data:ReviewBaseDB):
    try:
        return reviewCore.save_one(data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.get('/reviews/{pid}', name='Get a review', tags=['Wines review'], response_model=ReviewFullDB)
async def get_review(pid: str):
    try:
        return reviewCore.get_one(pid)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.patch('/reviews/{pid}', name='Update a review', tags=['Wines review'], response_model=MessageDB)
async def update_review(pid: str, data: ReviewBaseDB):
    try:
        return reviewCore.update_one(pid, data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.delete('/reviews/{pid}', name='Delete a review', tags=['Wines review'])
async def delete_review(pid: str):
    try:
        return reviewCore.delete_one(pid)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
