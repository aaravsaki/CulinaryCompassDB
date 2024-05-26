import init
import mail
from collections import defaultdict

supabase = init.get_client()

# generic insert statement execution
def execute_insert_statement(tablename: str, columns: list[str], values: list):
    data = {col: val for col, val in zip(columns, values)}
    return supabase.table(tablename).insert(data).execute()

def insert_email(key: str, io_mail: str):
    if mail.verify_email(key, io_mail):
        if len(execute_get("email", "mail", io_mail)) == 0:
            d_prob = mail.get_component("temp", io_mail, ["DeliverabilityConfidenceScore"])
            if d_prob:
                d_prob = d_prob[0]
                execute_insert_statement("email", ["mail", "delivery_prob"], [io_mail, d_prob])
                print("insertion is successful")
        else:
            print("email already exists")
    else:
        print("Invalid email")
    print()

# verifies that the user id exists in the database
def verify_id(name: str) -> bool:
    response = supabase.table("person").select("user_id").eq("username", name).execute()
    return len(response.data) != 0

# generic get statement execution; val: type of attr
def execute_get(tablename: str, attr_name: str = None, val = None):
    if val != None and attr_name != None:
        response = supabase.table(tablename).select("*").eq(attr_name, val).execute()
    elif val == None:
        response = supabase.table(tablename).select(attr_name).execute()
    else:
        response = supabase.table(tablename).select("*").execute()
    return response.data

def get_userid(tablename: str, username: str):
    response = supabase.table(tablename).select("user_id").eq("username", username).execute()
    return response.data[0]["user_id"]

def get_fooditem_id(user_name: str, food_name: str):
    fooditem_ids = supabase.rpc("get_item_ids", {"user_name": user_name, "food_name": food_name}).execute()
    return fooditem_ids.data

def delete_user(tablename: str, user_name: str):
    supabase.table(tablename).delete().eq('username', user_name).execute()

def get_day(user: str, day: str):
    response = supabase.rpc(f"get_day_schedule", {'user_name': user, 'day': day}).execute()
    data = dict()
    for meal in response.data:
        if meal["mealname"]:
            data[meal["mealname"]] = {
                "date" : meal["date"][:meal["date"].index('T')], 
                "fooditems": [],
                "time": meal["date"][meal["date"].index('T')+1:]
            }

            for fooditem in meal["fooditems"]:
                nutritional_info = supabase.rpc('get_nutrition_info', {'user_name': user, 'food_item': fooditem}).execute()
                if nutritional_info.data is not None:
                    nutritional_info = nutritional_info.data[0]
                    del nutritional_info["item_id"]
                    data[meal["mealname"]]["fooditems"].append(nutritional_info)
    
    data = {"Summary" : {"date": day, "fooditems": [create_nutrition_summary(user, day)]}} | data
    return data

def get_month(user: str, mon: int):
    response = supabase.rpc(f"get_month_schedule", {'user_name': user, 'month': mon}).execute()
    data = defaultdict(list)
    for meal in response.data:
        data[meal["date"][:meal["date"].index('T')]].append({meal["mealname"] : meal["fooditems"]})
    return data

def create_nutrition_summary(user: str, day: str):
    response = supabase.rpc("get_nutrition_summary", {"user_name": user, "day": day}).execute()
    data_dict = {"name" : "Nutrition Summary"} | {k: v for d in response.data for k, v in d.items()}
    return data_dict

def delete_fooditem(tablename: str, fooditem_id: int):
    supabase.table(tablename).delete().eq("item_id", fooditem_id).execute()

def delete_meal(tablename: str, meal_id: int):
    supabase.table(tablename).delete().eq("meal_id", meal_id).execute()

def get_meal_ids(date: str, meal_name: str, username: str):
    meal_ids = supabase.rpc("get_meal_ids", {'user_name': username, 'meal_name': meal_name, 'day': date}).execute()
    return meal_ids.data


