from fastapi import Depends, FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.routers import aiLab, company, evalution, jobRecommed, positionRecommed, resume, user
#解决跨域问题
origins = [
    "http://localhost", 
    "http://127.0.0.1", 
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:3000", # react+vite
    "http://localhost:5174",
]

# from .dependencies import get_query_token, get_token_header
from .routers import items,Login_v2,job 
from .utils.db import create_db_and_tables
# app = FastAPI(dependencies=[Depends(create_db_and_tables)])
app = FastAPI() 
# app.mount("/static", StaticFiles(directory="templates"), name="static")
app.mount("/static", StaticFiles(directory="dist"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()
    
    host_port = "redis-17507.c294.ap-northeast-1-2.ec2.cloud.redislabs.com:17507"
    password = "fyjlrtlyWZgdtxgSyyzhzODdfztle9My"
    url = f"redis://:{password}@{host_port}/0"
    # redis = aioredis.from_url("redis://redis-17507.c294.ap-northeast-1-2.ec2.cloud.redislabs.com:17507")
    redis = aioredis.from_url(url)
    try:
        pong = await redis.ping()
        print('Redis connected:', pong)
    except Exception as e:
        print('Redis connection failed:', e)

    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

# app.include_router(users.router)
app.include_router(items.router)
app.include_router(Login_v2.router)
app.include_router(job.router)
app.include_router(resume.router)
app.include_router(company.router)
app.include_router(user.router)
app.include_router(router=aiLab.router)

app.include_router(router=evalution.router)
app.include_router(positionRecommed.router)
app.include_router(jobRecommed.router)

# app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}