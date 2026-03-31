from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import (
    LineChartResponseModel,
    PieChartResponseModel,
    PopulationPyramidResponseModel,
    WaffleChartResponseModel,
)
from services import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/line-chart", response_model=LineChartResponseModel)
async def get_line_chart_data(
    region_id: int = Query(..., description="ID региона"),
    indicators: str = Query(..., description="Список названий показателей через запятую"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_line_chart_data(session=session, region_id=region_id, indicators=indicators)


@router.get("/pie-chart", response_model=PieChartResponseModel)
async def get_pie_chart_data(
    region_id: int = Query(..., description="ID региона"),
    indicators: str = Query(..., description="Список названий показателей через запятую"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_pie_chart_data(session=session, region_id=region_id, indicators=indicators)


@router.get("/population-pyramid", response_model=PopulationPyramidResponseModel)
async def get_population_pyramid(
    region_id: int = Query(..., description="ID региона"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_population_pyramid(session=session, region_id=region_id)


@router.get("/bar-chart-b", response_model=PopulationPyramidResponseModel)
async def get_bar_chart_b_data(
    region_id: int = Query(..., description="ID региона"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_population_pyramid(session=session, region_id=region_id)


@router.get("/waffle-chart", response_model=WaffleChartResponseModel)
async def get_waffle_chart_data(
    region_id: int = Query(..., description="ID региона"),
    indicators: str = Query(..., description="Список показателей и подпоказателей через запятую"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_waffle_chart_data(session=session, region_id=region_id, indicators=indicators)
