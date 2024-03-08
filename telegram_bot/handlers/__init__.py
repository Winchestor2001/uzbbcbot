from . import users
from . import admins


routers_list = [
    users.users.router,
    users.services.router,
]

__all__ = [
    "routers_list",
]

