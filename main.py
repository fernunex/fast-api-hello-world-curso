#Python
from typing import Optional

#Pydantic
from pydantic import BaseModel # to create models

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query

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
        description= "Just is the name of the person"),
    age: Optional[int] = Query(
        ..., # An obligatory query parameter is not recommended
        ge=18) 
):
    return {name: age}