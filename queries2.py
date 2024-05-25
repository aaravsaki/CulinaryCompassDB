import init

supabase = init.get_client()

def verify_id(name: str) -> bool:
    response = supabase.table("person").select("user_id").eq("username", name).execute()
    return len(response.data)

print(verify_id("test"))