from typing import List, Union
from fastapi import APIRouter, HTTPException

from app.models.review import ReviewBaseDB, ReviewFullDB
from app.core.review import ReviewCore
from app.models.message_db import MessageDB
from starlette.responses import JSONResponse

review_router = APIRouter()


@review_router.get('/reviews', name='List reviews', tags=['Wines review'], response_model=List[ReviewFullDB])
async def get_reviews(limit: Union[int, None] = 20, offset: Union[int, None] = 1, price: Union[str, None] = None, points: Union[str, None] = None):
    """
    Get all reviews
    """
    # price[lte]=200
    if limit < 0:
        return JSONResponse(content={
            "detail": "limit must be positive integer"
        }, status_code=422)
    if offset <= 0:
        return JSONResponse(content={
            "detail": "offset must be positive integer"
        }, status_code=422)

    filters = {}

    def get_filters(field_name: str, filters_str: str, filters_dict: dict):
        if filters_str is not None:
            filters_dict[field_name] = {}
            filters_str = filters_str.replace(", ", ",")
            for f in filters_str.split(','):
                if ":" not in f:
                    return JSONResponse(content={
                        "detail": "price parameter is invalid"
                    }, status_code=422)
                key, value = f.split(':')
                filters_dict[field_name][key] = float(value)
                if key not in ['$lt', '$gt', '$lte', '$gte', '$eq']:
                    return JSONResponse(content={
                        "detail": "price parameter is invalid"
                    }, status_code=422)
                if not value.isnumeric():
                    return JSONResponse(content={
                        "detail": "price parameter is invalid"
                    }, status_code=422)

        return filters_dict

    filters = get_filters("price", price, filters)
    filters = get_filters("points", points, filters)
    filters = {
        '$and': [
            filters
        ]
    }

    try:
        return ReviewCore.get_all(limit, offset, filters)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.post('/reviews', name='Create a review', tags=['Wines review'], response_model=MessageDB)
async def get(data: ReviewBaseDB):
    try:
        return ReviewCore.save_one(data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.get('/reviews/{pid}', name='Get a review', tags=['Wines review'], response_model=ReviewFullDB)
async def get_review(pid: str):
    try:
        return ReviewCore.get_one(pid)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.patch('/reviews/{pid}', name='Update a review', tags=['Wines review'], response_model=MessageDB)
async def update_review(pid: str, data: ReviewBaseDB):
    try:
        return ReviewCore.update_one(pid, data)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))


@review_router.delete('/reviews/{pid}', name='Delete a review', tags=['Wines review'])
async def delete_review(pid: str):
    try:
        return ReviewCore.delete_one(pid)
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
