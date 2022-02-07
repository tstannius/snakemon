from fastapi import APIRouter

from app.api.endpoints import auth, jobs, smk, workflows

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(smk.router, prefix="/smk", tags=["snakemake"])
api_router.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
