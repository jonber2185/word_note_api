from db.mySQL import run_sql


# 아이디 중복 확인
def get_user_id(user_id: str):
    return run_sql(
        "SELECT user_id FROM users WHERE user_id = %s",
        (user_id,),
        fetchone=True
    )

def create_user(user_id, hashed_password):
    run_sql(
        "INSERT INTO users (user_id, pw) VALUES (%s, %s)",
        (user_id, hashed_password),
    )
    # refresh_token 생성
    run_sql(
        "INSERT INTO refresh_tokens (user_id, refresh_token) VALUES (%s, %s)",
        (user_id, "new_refresh_token")
    )

def update_user_password(user_id: str, new_password: str):
    run_sql(
        "UPDATE users SET pw = %s WHERE user_id = %s",
        (new_password, user_id)
    )

def delete_user(user_id: str):
    run_sql(
        "UPDATE users SET deleted_at = NOW() WHERE user_id = %s",
        (user_id,)
    )
