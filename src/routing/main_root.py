from __future__ import annotations

from typing import TypedDict, List
from collections.abc import Callable

from views.dashboard_view import DashboardView
from views.settings_view import SettingsView
from views.login_view import LoginView
from views.home_view import HomeView


from .paths_type import PATHS_ROOT


class TypedRoute(TypedDict):
    path: PATHS_ROOT
    label: str
    icon: str
    component: Callable[[], None]


ROUTES_ROOT: List[TypedRoute] = [
    {
        "path": "/",
        "label": "Home",
        "icon": "home",
        "component": HomeView,
    },
    {
        "path": "/dashboard",
        "label": "Dashboard",
        "icon": "dashboard",
        "component": DashboardView,
    },
    {
        "path": "/settings",
        "label": "Impostazioni",
        "icon": "settings",
        "component": SettingsView,
    },
    {
        "path": "/login",
        "label": "Login",
        "icon": "login",
        "component": LoginView,
    },
]
