from fastapi import APIRouter, HTTPException
from app.services.athena_service import AthenaService

router = APIRouter(
    prefix="/api/v1/vehicles",
    tags=["Vehicles"]
)

athena_service = AthenaService()


@router.get("/{vin}")
def get_vehicle(vin: str):

    # Validate VIN
    if len(vin) != 17:
        raise HTTPException(
            status_code=422,
            detail="VIN must contain exactly 17 characters"
        )

    try:
        vehicle = athena_service.get_vehicle_by_vin(vin)

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Vehicle not found"
            )

        return {
            "message": "Vehicle details retrieved successfully",
            "data": vehicle
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unable to retrieve vehicle details"
        )