#Python
from typing import Optional, List
from enum import Enum

#Pydantic
from pydantic import BaseModel # to create models
from pydantic import Field, EmailStr, SecretStr

# FastAPI
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Body, Query, Path, Form, Header, Cookie, UploadFile, File
from fastapi import status

app = FastAPI()


# Models + Validations
class HairColor(str, Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blond = "blond"
    red = "red"


class Location(BaseModel):
    city: str= Field(
        ...,
        min_length=2,
        max_length=50
        )
    state: str = Field(
        ...,
        min_length=2,
        max_length=50
        )
    country: str = Field(
        ...,
        min_length=2,
        max_length=50
        )
    
    class Config: 
        schema_extra = {
        "example": {
            "city": "Salamanca",
            "state": "Monterrey",
            "country": "Mexico"}
            }

class PersonBase(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Saul'
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example='Valdez'
        )
    age: int = Field(
        ...,
        gt=0,
        le=115,
        example=19

    )
    email: EmailStr = Field(
        ...,
        example='som@thing.com'
        )
    hair_color: Optional[HairColor] = Field(default=None, example='blond')
    is_married: Optional[bool] = Field(default=None, example=False)

class Person(PersonBase):
    password: str = Field(..., min_length=8)
    # class Config:
    #     schema_extra = {
    #         "example":{
    #                 "first_name": "Fernando",
    #                 "last_name": "Nuñez Valdez",
    #                 "age": 20,
    #                 "email": "fer@example.com",
    #                 "hair_color": "black",
    #                 "is_married": False
    #         }
    #     }

class PersonOut(PersonBase):
    pass

class LoginOut(BaseModel):
    username: str = Field(
        ..., 
        max_length=20, 
        example="Fulanito55"
        )
    msg: str = Field(default="Login Successfully")

# PATH OPERATIONS

@app.get(
    path="/",
    status_code=status.HTTP_200_OK,
    tags=["Home"]
    )
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post(
    path="/person/new",
    response_model=PersonOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def create_person(person: Person = Body(...)): # "..."" means that the parameter is obligatory
    return person

# Validaciones: Query Parameters

@app.get(
    path="/person/detail",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    name: Optional[str] = Query(
        None, 
        min_length=1, 
        max_length=50,
        title="Person Name", 
        description= "Just is the name of the person. It's between 1 and 50 char",
        example="Laura"
        ),
    age: Optional[int] = Query(
        ..., # An obligatory query parameter is not recommended
        ge=18,
        title="Person Age",
        description="This is the person age. It's required",
        example=50
        ) 
):
    return {name: age}

# Validaciones: Path Parameters

# HTTPExceptions

persons = [1,2,3,4,5,6,7,8,9,10]

@app.get(
    path="/person/detail/{person_id}",
    status_code=status.HTTP_200_OK,
    tags=["Persons"]
    )
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="The ID is required to show the person's detail",
        example=859
        )
):
    if person_id not in persons:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This person_id does not exist."
        )
    return {person_id: "Exist!"}

# Validaciones: Request Body

@app.put(
    path="/person/{person_id}",
    status_code=status.HTTP_201_CREATED,
    tags=["Persons"]
    )
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
        example=999
    ),
    person: Person = Body(...),
    location: Location = Body(...,)
):
    result = person.dict()
    result.update(location.dict())

    return result

# Forms

@app.post(
    path='/login',
    status_code=status.HTTP_200_OK,
    response_model=LoginOut,
    tags=["Login-Logout"]
)
def login(
    username: str = Form(...),
    password: str = Form(...)
):
    return LoginOut(username=username)

# Cookies and Headers Parameters

@app.post(
    path="/contact",
    status_code=status.HTTP_200_OK,
    tags=["Contact"]
    )
def contact(
    first_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    last_name: str = Form(
        ...,
        max_length=20,
        min_length=1
    ),
    email: EmailStr = Form(...),
    message: str = Form(
        ...,
        min_length=20,
    ),
    user_agent: Optional[str] = Header(default=None),
    ads: Optional[str] = Cookie(default=None)
):
    return user_agent

# Files

@app.post(
    path="/post-image",
    status_code=status.HTTP_200_OK,
    tags=["Images"]
)
def post_image(
    image: UploadFile = File(...)
):
    return {
        "Filename": image.filename,
        "Type": image.content_type,
        "Size kB": str(round(len(image.file.read())/1024,ndigits=1)) + "KB"
    }

@app.post(
    path="/post-images",
    status_code=status.HTTP_200_OK,
    tags=["Images"]
)
def post_images(
    images: List[UploadFile] = File(...)
):
    info_images = [
        {
            "Filename": image.filename,
            "Content_type": image.content_type,
            "Size":  str(round(len(image.file.read())/1024,ndigits=1)) + "KB"
        }
        for image in images]
    return info_images