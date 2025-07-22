# from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager

from src.router import router
from src.container import AppContainer


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = Redis.from_url(
        "redis://:abc123@redis:6379", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="rs-cache")
    yield
    
def load_middleware() -> list[Middleware]:
    ...

def create_app() -> FastAPI:
    container = AppContainer()
    app_ = FastAPI(
        title="LangGraph Practical API",
        description="FastAPI with dependency injection",
        lifespan=lifespan,
        # middleware=load_middleware,
        debug=True
    )
    
    # 이 부분이 의존성 주입을 활성화
    container.wire(
        packages=["src.domain"], # 폴더 단위
        modules=["src.router"] # 파일 단위 
    )

    app_.include_router(router)
    app_.container = container # 앱 인스턴스에 DI 컨테이너를 할당
    return app_ 


app = create_app()


