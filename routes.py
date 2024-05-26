from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from datetime import datetime
import queries

USER_TABLE = 'person'
MEAL_TABLE = 'meal'
FOODITEM_TABLE = 'fooditem'
MEALHAS_TABLE = 'meal_has'
PERSONHAS_TABLE = 'person_fooditem'

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

    frequency: dict[int, int]

    username: str

    date: str

class MonthSchedule(BaseModel):
    username: str

    month: int

class DaySchedule(BaseModel):
    username: str
    
    day: str = Field(default=f'{datetime.now().year}-{datetime.now().month}-{datetime.now().day}')

class MealFoodAssociation(BaseModel):
    meal_id: int

    food_id: int

class Email(BaseModel):
    mail: str

class MealDeletion(BaseModel):
    username: str

    date: str

    name: str

class ItemDeletion(BaseModel):
    username: str

    name: str


@app.get("/verify/")
def verify(username: str):
    return {"exists": queries.verify_id(username)}

@app.post("/register/")
def create_user(user: User):
    data = user.model_dump()
    return queries.execute_insert_statement(USER_TABLE, list(data.keys()), list(data.values()))

@app.post("/month/")
def get_month(schedule: MonthSchedule):
    data = schedule.model_dump()
    return queries.get_month(data["username"], data["month"])

@app.post("/day/")
def get_day(schedule: DaySchedule):
    data = schedule.model_dump()
    return queries.get_day(data["username"], data["day"])

@app.post("/create/food_item/")
def create_fooditem(fooditem: FoodItem):
    data = fooditem.model_dump()
    response = queries.execute_insert_statement(FOODITEM_TABLE, list(data.keys()), list(data.values()))
    return {"item_id": response.data[0]["item_id"]}

@app.post("/create/meal/")
def create_meal(meal: Meal):
    user_id = int(queries.get_userid(USER_TABLE, meal.username))
    meal_id = queries.execute_insert_statement(MEAL_TABLE, ['name', 'date', 'user_id'], [meal.name, meal.date, user_id]).data[0]["meal_id"]

    for fooditem_id, occurrences in meal.frequency.items():
        queries.execute_insert_statement(MEALHAS_TABLE, ['meal_id', 'food_id', 'amount'], [meal_id, fooditem_id, occurrences])
        queries.execute_insert_statement(PERSONHAS_TABLE, ['food_id', 'user_id'], [fooditem_id, user_id])

    return meal_id

@app.post("/create/meal_has/")
def create_meal_food_assoc(association: MealFoodAssociation):
    data = association.model_dump()
    response = queries.execute_insert_statement(MEALHAS_TABLE, list(data.keys()), list(data.values()))
    return response

@app.post("/create/email/")
def create_email(io_mail: Email):
    queries.insert_email("404", io_mail.mail)

@app.post("/delete/user/")
def delete_user(user: User):
    queries.delete_user(USER_TABLE, user.username)
    return

@app.post("/delete/fooditem/")
def delete_fooditem(delete_request: ItemDeletion):
    fooditem_ids = queries.get_fooditem_id(delete_request.username, delete_request.name)
    for fooditem in fooditem_ids:
        fooditem_id = fooditem["item_id"]
        queries.delete_fooditem(FOODITEM_TABLE, fooditem_id)

@app.post("/delete/meal/")
def delete_meal(delete_request: MealDeletion):
    meal_ids = queries.get_meal_ids(delete_request.date, delete_request.name, delete_request.username)
    for meal in meal_ids:
        meal_id = meal["item_id"]
        queries.delete_meal(MEAL_TABLE, meal_id)

@app.post("/all_fooditems/")
def get_allfooditems(user: str):
    return queries.get_all_fooditems(user)

@app.post("/fooditem_id/")
def get_fooditem_id(user: str, food_name: str):
    return queries.get_fooditem_id(user, food_name)
