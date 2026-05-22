from typing import List

from routing.route_interfaces import TypedRouteChildrenValue
from typing_extensions import Literal
from views.dashboard_main import DashboardMain
from views.profile_view import ProfileView
from views.report_view import ReportView
from views.security_view import SecurityView
from views.settings_main import SettingsMain
from views.statistics_view import StatisticsView

PARENT_CHILDREN = Literal[
    "DASHBOARD_CHILDREN", "SETTINGS_CHILDREN"
]  # = ChildrenRegistry.DASHBOARD_CHILDREN, ChildrenRegistry.SETTINGS_CHILDREN


class ChildrenRegistry:
    DASHBOARD_CHILDREN: List[TypedRouteChildrenValue] = [
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
        },
    ]

    SETTINGS_CHILDREN: List[TypedRouteChildrenValue] = [
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
        },
    ]

    @classmethod
    def as_nicegui_dict(cls, section: PARENT_CHILDREN):
        """Formatta i dati esattamente come li vuole ui.sub_pages"""
        data = getattr(cls, section, [])
        return {item["path"]: item["component"] for item in data}

    @classmethod
    def get_childrens_list(cls):
        """Formatta i dati esattamente come li vuole ui.sub_pages"""
        attributi = [
            a for a in dir(cls) if not callable(getattr(cls, a)) and not a.startswith("__")
        ]
        return attributi
