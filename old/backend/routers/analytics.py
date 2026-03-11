from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import LineChartResponseModel, PieChartResponseModel, PopulationPyramidResponseModel
from services import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/line-chart", response_model=LineChartResponseModel)
async def get_line_chart_data(
    region_id: int = Query(..., description="ID региона"),
    indicator_ids: str = Query(..., description="Список ID показателей"),
    session: Session = Depends(get_db),
):
    indicator_ids_list = [int(x) for x in indicator_ids.split(",")]
    service = AnalyticsService()
    return service.get_line_chart_data(session=session, region_id=region_id, indicator_ids=indicator_ids_list)


@router.get("/pie-chart", response_model=PieChartResponseModel)
async def get_pie_chart_data(
    region_id: int = Query(..., description="ID региона"),
    indicator_ids: list[int] = Query(..., description="Список ID показателей для сегментов pie"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_pie_chart_data(session=session, region_id=region_id, indicator_ids=indicator_ids)


@router.get("/population-pyramid", response_model=PopulationPyramidResponseModel)
async def get_population_pyramid(
    region_id: int = Query(..., description="ID региона"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_population_pyramid(session=session, region_id=region_id)
