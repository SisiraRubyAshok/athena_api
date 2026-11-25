from fastapi import FastAPI

from app.routes import vehicle

app = FastAPI(
    title="Vehicle Details API",
    description="API to retrieve vehicle information from Amazon Athena using VIN",
    version="1.0.0"
)


app.include_router(vehicle.router)


@app.get("/")
def home():

    return {
        "message": "Vehicle Details API is running"
    }