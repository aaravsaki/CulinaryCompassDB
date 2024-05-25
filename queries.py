import init

supabase = init.get_client()

def execute_insert_statement(tablename: str, columns: list[str], values: list[str]):
    data = {col: val for col, val in zip(columns, values)}
    supabase.table(tablename).upsert(data).execute()


