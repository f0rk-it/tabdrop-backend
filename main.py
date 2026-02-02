from fastapi import FastAPI
from app.config import settings
from app.core.middleware import setup_middleware
from app.api.router import router


app = FastAPI(
    title=settings.APP_NAME,
    description='FastAPI backend for TabDrop'
)

setup_middleware(app)

app.include_router(router, prefix='/api')

@app.get('/')
async def root():
    return {'message': f'Welcome to fastAPI backend for {settings.APP_NAME}'}