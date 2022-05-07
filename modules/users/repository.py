from app import database
from libs.base_repo import BaseModelRepository

from .models import User
from .tables import users


class UserRepository(BaseModelRepository[User]):
    pass


users_repo = UserRepository(
    db=database,
    model_class=User,
    table=users,
    pk_field=users.c.id,
)
