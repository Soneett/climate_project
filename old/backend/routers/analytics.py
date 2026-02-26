from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from models import ChartDataResponseModel, PopulationPyramidResponseModel
from services import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/chart_data", response_model=ChartDataResponseModel)
async def get_chart_data(
    region_id: int = Query(..., description="ID региона"),
    indicator_ids: list[int] = Query(..., description="Список ID показателей"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_chart_data(
        session=session,
        region_id=region_id,
        indicator_ids=indicator_ids,
    )


@router.get("/population_pyramid", response_model=PopulationPyramidResponseModel)
async def get_population_pyramid(
    region_id: int = Query(..., description="ID региона"),
    year: int | None = Query(None, description="Год (если не указан, берется последний доступный)"),
    session: Session = Depends(get_db),
):
    service = AnalyticsService()
    return service.get_population_pyramid(
        session=session,
        region_id=region_id,
        year=year,
    )
