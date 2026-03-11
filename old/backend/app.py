from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import engine
from database_views import create_reporting_views
from tables.base import Base

from routers import (
    regions_router,
    units_router,
    indicator_subtypes_router,
    indicators_router,
    data_sources_router,
    indicator_values_router,
    population_age_sex_router,
    regional_programs_router,
    program_regions_router,
    events_router,
    analytics_router,
)

from scripts.fill_db import main

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    main()  
    create_reporting_views(engine)
    print("Database tables and views created!")
    yield
    print("Shutting down...")

app = FastAPI(
    title="Climate Profile Backend Service",
    description="API для работы с климатическими и региональными данными",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_model=str)
async def read_root():
    return "Climate Profile Backend Service - API Documentation available at /docs"

@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья приложения"""
    return {
        "status": "healthy",
        "service": "climate-profile-backend",
        "version": "1.0.0"
    }

@app.get("/api-info")
async def api_info():
    """Информация о доступных API endpoint'ах"""
    return {
        "name": "Climate Profile Backend Service",
        "description": "API для работы с региональными, климатическими и демографическими данными",
        "version": "1.0.0",
        "endpoints": {
            "regions": "/regions",
            "units": "/units",
            "indicators": "/indicators",
            "indicator_values": "/indicator_values",
            "population_data": "/population",
            "programs": "/programs",
            "events": "/events",
            "data_sources": "/data_sources",
            "indicator_subtypes": "/indicator_subtypes",
            "program_region_links": "/program_regions",
            "analytics": {
                "line_chart": "/analytics/line-chart",
                "pie_chart": "/analytics/pie-chart",
                "population_pyramid": "/analytics/population-pyramid"
            },
        },
        "documentation": "/docs",
        "redoc": "/redoc"
    }

app.include_router(regions_router)
app.include_router(units_router)
app.include_router(indicator_subtypes_router)
app.include_router(indicators_router)
app.include_router(data_sources_router)
app.include_router(indicator_values_router)
app.include_router(population_age_sex_router)
app.include_router(regional_programs_router)
app.include_router(program_regions_router)
app.include_router(events_router)
app.include_router(analytics_router)

if __name__ == "__main__": 
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
