from __future__ import annotations

from collections.abc import Callable
from typing import Literal, TypedDict, List




from views.profile_view import ProfileView
from views.security_view import SecurityView

from views.report_view import ReportView
from views.statistics_view import StatisticsView


from .paths_type import PATHS_ROOT

PATHS_CHILDRENS: Literal["/dashboard/report", "/dashboard/statistics", "/settings/security", "/settings/profile"]

# PATHS_CHILDRENS: Literal["/report", "/statistics", "/security", "/profile"]


class TypedRouteChildrenValue(TypedDict):
    path: str
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
                "path": "/dashboard/report",
                "label": "Report",
                "icon": "report",
                "component": ReportView,
                
            },
            {
                "path": "/dashboard/statistics",
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
                "path": "/settings/security",
                "label": "Security",
                "icon": "security",
                "component": SecurityView,
                
            },
            {
                "path": "/settings/profile",
                "label": "Profile",
                "icon": "profile",
                "component": ProfileView,
            }

        ]
    }
]









