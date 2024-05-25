import init
import mail

supabase = init.get_client()

# generic insert statement execution
def execute_insert_statement(tablename: str, columns: list[str], values: list[str]):
    data = {col: val for col, val in zip(columns, values)}
    supabase.table(tablename).upsert(data).execute()

def insert_email(key: str, io_mail: str):
    if mail.verify_email(key, io_mail):
        if len(execute_get("email", "mail", io_mail)) == 0:
            d_prob = mail.get_component("temp", io_mail, ["DeliverabilityConfidenceScore"])[0]
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
def execute_get(tablename: str, attr_name: str, val):
    response = supabase.table(tablename).select("*").eq(attr_name, val).execute()
    return response.data

def get_day(user: str, day: str):
    response = supabase.rpc(f"get_day_schedule", {'username': user, 'day': day}).execute()
    data = dict()
    for meal in response.data:
        data[meal["mealname"]] = {
            "date" : meal["date"][:meal["date"].index('T')], 
            "fooditems": meal["fooditems"], 
            "time": meal["date"][meal["date"].index('T')+1:]
        }
    return data

def get_month(user: str, mon: int):
    response = supabase.rpc(f"get_month_schedule", {'username': user, 'month': mon}).execute()
    return {meal["mealname"] : {"date" : meal["date"][:meal["date"].index('T')], "fooditems": meal["fooditems"]} for meal in response.data}



