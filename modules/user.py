import re as _re
import errors.base as _errors
from db import modules as _db_modules
from .auth import hash_password as _hash_password


# 조건 정규표현식
allowed_id_pattern = r'^[A-Za-z0-9._-]+$'
allowed_pw_pattern = r'^[A-Za-z0-9!@#$%^&*()\-_+=\[\]{}:;,.?]+$'

# 아이디 조건 확인
def is_valid_user_id(user_id: str):
    if len(user_id) < 4:
        raise _errors.UserValidationError("ID must be at least 4 characters long.")
    if len(user_id) > 30:
        raise _errors.UserValidationError("ID must be 30 characters or less.")
    if ' ' in user_id:
        raise _errors.UserValidationError("ID cannot contain spaces.")
    if not _re.match(allowed_id_pattern, user_id):
        raise _errors.UserValidationError("Invalid ID format.")
    
# 아이디 중복 확인
def is_unique_user_id(user_id: str):
    result = _db_modules.users.get_user_id(user_id)
    if result is not None: raise _errors.UserUniqueError()

# pw 조건 확인
def is_valid_password(password: str):
    if len(password) < 8:
        raise _errors.UserValidationError("Password must be at least 8 characters long.")
    if ' ' in password:
        raise _errors.UserValidationError("Password cannot contain spaces.")
    if not _re.match(allowed_pw_pattern, password):
        raise _errors.UserValidationError("Invalid password format.")


def create_user(user_id, password):
    is_valid_user_id(user_id) # id 형식 확인
    is_unique_user_id(user_id) # id 중복 확인
    is_valid_password(password) # pw 형식 확인

    _db_modules.users.create_user(
        user_id=user_id, 
        hashed_password=_hash_password(password)
    )

def update_user_password(user_id: str, new_password: str):
    is_valid_password(new_password) # pw 형식 확인
    _db_modules.users.update_user_password(
        user_id=user_id,
        new_password=_hash_password(new_password)
    )

def delete_user(user_id: str):
    _db_modules.users.delete_user(user_id)