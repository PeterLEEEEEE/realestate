# from redis import asyncio as aioredis
from redis.asyncio.client import Redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi.middleware import Middleware
from contextlib import asynccontextmanager
from fastmcp import FastMCP

from src.router import router
from src.container import AppContainer
from src.core.mcp import register_basic_tools


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    redis = Redis.from_url(
        "redis://:abc123@redis:6379", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="rs-cache")
    yield
    
def load_middleware() -> list[Middleware]:
    ...
    
# Create MCP server
mcp = FastMCP("Tools")
register_basic_tools(mcp)
mcp_app = mcp.http_app(path='/v1')


@asynccontextmanager
async def combined_lifespan(app: FastAPI):
    async with app_lifespan(app):
        async with mcp_app.lifespan(app):
            yield

def create_app() -> FastAPI:
    container = AppContainer()
    app_ = FastAPI(
        title="LangGraph Realestate Agent API",
        description="FastAPI with dependency injection",
        lifespan=combined_lifespan,
        # middleware=load_middleware,
        debug=True
    )
    app_.mount("/mcp", mcp_app)
    # 이 부분이 의존성 주입을 활성화
    container.wire(
        packages=["src.domain"], # 폴더 단위
        modules=["src.router"] # 파일 단위 
    )

    app_.include_router(router)
    app_.container = container # 앱 인스턴스에 DI 컨테이너를 할당
    return app_ 


app = create_app()


