import init

supabase = init.get_client()

# generic insert statement execution
def execute_insert_statement(tablename: str, columns: list[str], values: list[str]):
    data = {col: val for col, val in zip(columns, values)}
    supabase.table(tablename).upsert(data).execute()

# verifies that the user id exists in the database
def verify_id(name: str) -> bool:
    response = supabase.table("person").select("user_id").eq("username", name).execute()
    return len(response.data) != 0

# generic get statement execution
def execute_get(tablename: str, attr_name: str, pid: int):
    response = supabase.table(tablename).select("*").eq(attr_name, pid).execute()
    return response.data

def get_month(user: str, mon: int):
    response = supabase.rpc(f"get_month_schedule", {'username': user, 'month': mon}).execute()
    for meal in response.data:
        return {meal["mealname"] : {"date" : meal["date"], "fooditems": meal["fooditems"]}}



