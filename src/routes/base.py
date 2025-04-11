from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]    
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)): 
    # Depends(get_settings): Ensure to import get_settings from your config module and already exist, this make fastapi more efficient and faster

    app_name = app_settings.APP_NAME
    app_version = app_settings.APP_VERSION
    
    return {
        "app_name": app_name,
        "app_version": app_version,
    }
