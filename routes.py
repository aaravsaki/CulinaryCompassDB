from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime

import queries

USER_TABLE = 'user'
MEAL_TABLE = 'meal'
FOODITEM_TABLE = 'fooditem'
HAS_TABLE = 'meal_has'

origins = [
    "http://localhost:5173"
    # Eventually put front-end url here
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(BaseModel):
    username: str

class FoodItem(BaseModel):
    # TODO: Change default to None instead of 0

    name: str

    calories: int = Field(default=0)
    
    protein: int = Field(default=0)

    fat: int = Field(default=0)

    carbs: int = Field(default=0)

    fiber: int = Field(default=0)

    sodium: int = Field(default=0)

    cholesterol: int = Field(default=0)

    vitamin_a: int = Field(default=0)

    vitamin_b: int = Field(default=0)

    vitamin_c: int = Field(default=0)

    vitamin_d: int = Field(default=0)

    vitamin_e: int = Field(default=0)

    vitamin_k: int = Field(default=0)

    zinc: int = Field(default=0)

    potassium: int = Field(default=0)

    magnesium: int = Field(default=0)

    calcium: int = Field(default=0)

    iron: int = Field(default=0)

    selenium: int = Field(default=0)

class Meal(BaseModel):
    name: str

    user_id: int

    date: datetime

class UserSchedule(BaseModel):
    username: str

    month: int

@app.get("/verify/")
def verify(username: str):
    return {"exists": queries.verify_id(username)}

@app.post("/register/")
def create_user(user: User):
    queries.execute_insert_statement(USER_TABLE, ['username'], [user.username])
    return user

@app.post("/month/")
def get_month(schedule: UserSchedule):
    data = schedule.model_dump()
    return queries.get_month(data["username"], data["month"])

@app.post("/create/food_item/")
def create_fooditem(fooditem: FoodItem):
    data = fooditem.model_dump()
    queries.execute_insert_statement(FOODITEM_TABLE, list(data.keys()), list(data.values()))
    return fooditem

@app.post("/create/meal/")
def create_meal(meal: Meal):
    data = meal.model_dump()
    queries.execute_insert_statement(MEAL_TABLE, list(data.keys()), list(data.values()))
    return meal


    
