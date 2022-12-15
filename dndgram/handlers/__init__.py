__all__ = [
    'dp', 'router_start', 'router_back', 'router_menu', 'router_profile',
    'router_age', 'router_gender', 'router_preferences', 'router_bio',
    'router_location'
]

from .start import dp, router_start
from .menu import router_menu
from .profile import router_profile
from .back import router_back
from .age import router_age
from .gender import router_gender
from .preferences import router_preferences
from .bio import router_bio
from .location import router_location

__routers__ = [
    router_start, router_menu, router_back, router_profile, router_age,
    router_gender, router_preferences, router_bio, router_location
]
