from fastapi import FastAPI, Query, Path, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from database import cars


class Car(BaseModel):
    make: str
    model: str
    year: int = Field(
        ..., ge=1970, lt=2022
    )  # constrain the value of year to be greater than 1970 and less then 2022
    price: float
    engine: Optional[str] = "V4"
    autonomous: bool
    sold: List[str]


app = FastAPI()


@app.get("/")
def root():
    return {"hello world": "i am the value of the msg"}


@app.get("/cars", response_model=List[Dict[str, Car]])
def get_cars(number: Optional[str] = Query("10", max_length=3)):
    response = []
    for id, car in list(cars.items())[: int(number)]:
        to_add = {}
        to_add[str(id)] = car
        response.append(to_add)
    return response


@app.get("/cars/{id}", response_model=Car)
def get_car_by_id(id: int = Path(..., ge=0, lt=1000)):
    car = cars.get(id)
    if not car:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"could not find car with {id=}",
        )
    return car
