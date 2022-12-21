#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel # to create models
from pydantic import Field

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models + Validations
class HairColor(str, Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blond = "blond"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    age: int = Field(
        ...,
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)): # "..."" means that the parameter is obligatory
    return person

# Validaciones: Query Parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name", 
        description= "Just is the name of the person. It's between 1 and 50 char"
        ),
    age: Optional[int] = Query(
        ..., # An obligatory query parameter is not recommended
        ge=18,
        title="Person Age",
        description="This is the person age. It's required"
        ) 
):
    return {name: age}

# Validaciones: Path Parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="The ID is required to show the person's detail"
        )
):
    return {person_id: "Exist!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    result = person.dict()
    result.update(location.dict())

    return result