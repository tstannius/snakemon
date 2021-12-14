from fastapi import APIRouter

from app.api.endpoints import smk, workflows

api_router = APIRouter()
api_router.include_router(smk.router, tags=["snakemake"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])