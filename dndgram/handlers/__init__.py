__all__ = [
    'dp', 'router_menu', 'router_profile', 'router_age', 'router_back'
]

from .start import dp
from .menu import router_menu
from .profile import router_profile
from .back import router_back
from .age import router_age

__routers__ = [
    router_menu, router_profile, router_age, router_back
]
