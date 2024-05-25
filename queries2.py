import init

supabase = init.get_client()

#verifies that the user id exists in the database
def verify_id(name: str) -> bool:
    response = supabase.table("person").select("user_id").eq("username", name).execute()
    return len(response.data) != 0

#gets the rows pertaining to meals
def get_meal(mid: int):
    response = supabase.table("meal").select("*").eq("meal_id", mid).execute()
    return response.data

#gets the rows pertaining to the fooditem
def get_fooditem(fid: int):
    response = supabase.table("fooditem").select("*").eq("item_id", fid).execute()
    return response.data

#gets rows pertaining to meal_has
def get_foods(mid: int):
    response = supabase.table("meal_has").select("*").eq("meal_id", mid).execute()
    return response.data