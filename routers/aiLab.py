from fastapi import APIRouter, FastAPI
from fastapi.responses import StreamingResponse
import time
from ..utils.ai_api import answer_with_stream
router = APIRouter(
    tags=["AI Lab"],
    # dependencies=[Depends(get_current_active_user)],
    responses={404: {"description": "Not found"}},
)
""" 
def event_stream():
    # 这是一个生成器函数，每次调用都会生成新的事件
    for i in range(50):
        #暂停1秒
        time.sleep(1)
        yield f"data: {i}\n\n"  # SSE 格式的事件 
"""

""" @router.get("/aiLab",response_class=StreamingResponse)
async def answer(inputToken :str):
    # return StreamingResponse(answer_with_stream(inputToken) , media_type="text/event-stream")
    return StreamingResponse(answer_with_stream(inputToken) )
 """

@router.get("/aiLab",)
def answer(inputToken :str):
    # return StreamingResponse(answer_with_stream(inputToken) , media_type="text/event-stream")
    res = {"message": answer_with_stream(inputToken)}
    return res