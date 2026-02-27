import errors.base as _errors
from db import modules as _db_modules

def create_set(set_id, title, description, owner_id, is_public):
    if len(title) > 100:
        raise _errors.SetValidationError("title must be 100 characters or less.")
    if len(description) > 250:
        raise _errors.SetValidationError("title must be 250 characters or less.")

    _db_modules.sets.create_set(
        set_id=set_id,
        title=title,
        description=description,
        is_public=is_public,
        owner_id=owner_id,
    )

from db.modules.sets import (get_user_set, get_user_sets)