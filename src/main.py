from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager

# @app.on_event("startup")
# async def startup_db_client():
#     settings = get_settings()

#     app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL) # MongoDB connection
#     app.db_client = app.mongo_conn[settings.MONGODB_DATABASE] # MongoDB database

# @app.on_event("shutdown")
# async def shutdown_db_client():
#     app.mongo_conn.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL) # MongoDB connection
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE] # MongoDB database

    yield
    app.mongo_conn.close()
    
app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
