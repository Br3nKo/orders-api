from fastapi import FastAPI
from app.api.routes.router import router
from fastapi.middleware.cors import CORSMiddleware
from app.database import sessionmanager
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()

app = FastAPI(lifespan=lifespan,)
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)
    
@app.get("/")
async def help():
    return {"message": "server is running - visit /docs for API documentation"}
