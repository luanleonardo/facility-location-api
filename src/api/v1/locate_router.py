from fastapi import APIRouter, HTTPException, Response, status
from pydantic import ValidationError

from src.api.schemas.locate import LocationRequest
from src.models import SolutionStatus
from src.services import solve_facility_location

router = APIRouter()


@router.post("/locate")
async def locate(locate_request: LocationRequest):
    try:
        location_solution = solve_facility_location(
            location_request=locate_request
        )

        if location_solution.status == SolutionStatus.INFEASIBLE:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=location_solution.message,
            )

        return Response(
            content=location_solution.model_dump_json(),
            media_type="application/json",
            status_code=status.HTTP_200_OK,
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=e.errors()
        )
