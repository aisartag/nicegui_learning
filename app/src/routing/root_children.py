from __future__ import annotations

from collections.abc import Callable
from typing import TypedDict, List




from views.dashboard_main import DashboardMain
from views.profile_view import ProfileView
from views.security_view import SecurityView

from views.report_view import ReportView
from views.settings_main import SettingsMain
from views.statistics_view import StatisticsView


from .paths_type import PATHS_ROOT, PATHS_CHILDRENS






class TypedRouteChildrenValue(TypedDict):
    path: PATHS_CHILDRENS
    label: str
    icon: str
    component: Callable[[], None]

class TypedRouteChildren(TypedDict):
    root: PATHS_ROOT
    childrens: List[TypedRouteChildrenValue]




ROUTES_ROOT_CHILDREN: List[TypedRouteChildren] = [
    {
        "root": "/dashboard",
        "childrens":  [
            {
                "path": "/",
                "label": "Dashboard Main",
                "icon": "",
                "component": DashboardMain,
                
            },
            {
                "path": "/report",
                "label": "Report",
                "icon": "report",
                "component": ReportView,
                
            },
            {
                "path": "/statistics",
                "label": "Statistics",
                "icon": "statistics",
                "component": StatisticsView,
            }

        ]
    },
    {
        "root": "/settings",
        "childrens":  [
              {
                "path": "/",
                "label": "SettingsMain",
                "icon": "",
                "component": SettingsMain,
                
            },
            {
                "path": "/security",
                "label": "Security",
                "icon": "security",
                "component": SecurityView,
                
            },
            {
                "path": "/profile",
                "label": "Profile",
                "icon": "profile",
                "component": ProfileView,
            }

        ]
    }
]









