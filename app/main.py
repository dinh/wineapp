from starlette.responses import JSONResponse, RedirectResponse
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from app.project import info

from app.routers.review import review_router

guinicorn_pid = None
origins = ["*"]

description = """
The Wine Review APIs provide CRUD functionalities for the wine dataset from [Kaggle](https://www.kaggle.com/datasets/zynicide/wine-reviews)

"""

tags_metadata = [
    {
        "name": "Wines review",
        "description": "CRUD API for the wine dataset",
    }
]

app = FastAPI(
    title=info['name'],
    version=info['version'],
    description=description,
    openapi_tags=tags_metadata,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


@app.get("/")
def root():
    return RedirectResponse(url="/api/docs")


@app.get('/api/healthcheck')
def healthcheck():
    return JSONResponse(content={"detail": "OK"})


@app.get('/api/info')
async def app_info():
    """Return model information"""
    return JSONResponse(content={
        "name": info['name'],
        "version": info['version'],
        "description": "Wine review API"
    })


app.include_router(review_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        app,
        host=info['address'],
        port=info['port']
    )
