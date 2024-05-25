from fastapi import FastAPI
from pydantic import BaseModel

import queries
import queries2

app = FastAPI()

USER_TABLE = 'user'
MEAL_TABLE = 'meal'
FOODITEM_TABLE = 'fooditem'
HAS_TABLE = 'meal_has'

class User(BaseModel):
    username: str

@app.get("/verify/")
def verify(username: str):
    return {"exists": queries2.verify_id(username)}

@app.post("/register/")
def create_user(user: User):
    queries.execute_insert_statement(USER_TABLE, ['username'], [user.username])
    return user

    
