from db.mySQL import run_sql

def create_set(set_id, title, description, owner_id, is_public):
    run_sql(
        "INSERT INTO sets (id, title, description, owner_id, is_public) VALUES (%s, %s, %s, %s, %s)",
        (set_id, title, description, owner_id, is_public),
    )

def get_user_sets(user_id) -> list:
    result = run_sql(
        "SELECT title, is_public, created_at FROM sets WHERE owner_id = %s",
        (user_id,),
    )
    if result is None: return []
    else: return result

def get_user_set(set_id, user_id):
    result = run_sql(
        "SELECT * FROM sets WHERE id = %s AND owner_id = %s",
        (set_id, user_id),
        fetchone=True
    )
    if result is None: return {}
    else: return result
