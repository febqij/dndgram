__all__ = [
    'dp', 'router_start', 'router_menu', 'router_profile', 'router_age',
    'router_back', 'router_gender'
]

from .start import dp, router_start
from .menu import router_menu
from .profile import router_profile
from .back import router_back
from .age import router_age
from .gender import router_gender

__routers__ = [
    router_start, router_menu, router_profile, router_age, router_back,
    router_gender
]
