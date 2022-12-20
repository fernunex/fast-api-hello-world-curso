#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel # to create models

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

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
