from typing import Union , Optional

from pydantic import BaseModel
from fastapi import UploadFile, File, Response
from typing import List
# app = FastAPI()
from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

router = APIRouter()
@router.post("/upload")
async def upload_file(file: UploadFile ):
    file_contents = await file.read()
    # 你可以在这里处理文件内容，例如保存到磁盘或者存储到数据库
    #保存到磁盘
    with open(file.filename, "wb") as f:
        f.write(file_contents)
    return {"filename": file.filename}