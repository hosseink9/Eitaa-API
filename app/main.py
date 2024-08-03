from fastapi import FastAPI
from api_v1.routers import router as eitaa_router

app = FastAPI()
app.include_router(router=eitaa_router, prefix='')