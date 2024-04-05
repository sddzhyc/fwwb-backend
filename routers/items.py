from typing import Union , Optional

from pydantic import BaseModel
from fastapi import UploadFile, File, Response
from typing import List
# app = FastAPI()
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache
router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/{item_id}")
@cache()
def read_item(item_id: int, q2: Union[str, None] = None):
    return {"item_id": item_id, "q": q2}


@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_price": item.price, "item_id": item_id}


@router.post("/login")
async def login(username: str, password: str, vertify: Optional[str] = None):
    return {"username": username, "password": password}