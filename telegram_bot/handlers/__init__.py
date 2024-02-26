from . import users
from . import admins


routers_list = [
    users.users.user_route,
]

__all__ = [
    "routers_list",
]

