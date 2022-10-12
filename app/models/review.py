from pydantic import BaseModel, Field
from app.repository.pyobjectid import PyObjectId
from bson import ObjectId
from typing import Optional


# `ReviewBaseDB` is a `BaseModel` that has the following fields:
#
# - `points`: an integer
# - `title`: a string
# - `description`: a string
# - `taster_name`: a string, but it can be `None`
# - `taster_twitter_handle`: a string, but it can be `None`
# - `price`: a float, but it can be `None`
# - `designation`: a string, but it can be `None`
# - `variety`: a string, but it can be `None`
# - `region_1`: a string, but it can be `None`
# - `region_2`: a string, but it can be `None`
# - `province`: a string, but it can be `None`
# - `country`: a string, but it can be `None
class ReviewBaseDB(BaseModel):
    points: int
    title: str
    description: str
    taster_name: Optional[str] = None
    taster_twitter_handle: Optional[str] = None
    price: Optional[float] = None
    designation: Optional[str] = None
    variety: Optional[str] = None
    region_1: Optional[str] = None
    region_2: Optional[str] = None
    province: Optional[str] = None
    country: Optional[str] = None
    winery: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "points": "87",
                "title": "Kirkland Signature 2011 Mountain Cuvée Cabernet Sauvignon (Napa Valley)",
                "description": "Soft, supple plum envelopes an oaky structure in this Cabernet, supported by 15% "
                               "Merlot. Coffee and chocolate complete the picture, finishing strong at the end, "
                               "resulting in a value-priced wine of attractive flavor and immediate accessibility.",
                "taster_name": "Virginie Boone",
                "taster_twitter_handle": "@vboone",
                "price": 19,
                "designation": "Mountain Cuvée",
                "variety": "Cabernet Sauvignon",
                "region_1": "Napa Valley",
                "region_2": "Napa",
                "province": "California",
                "country": "US",
                "winery": "Kirkland Signature"
            }
        }

class ReviewFullDB(ReviewBaseDB):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
