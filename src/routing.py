from __future__ import annotations

from typing import NotRequired, TypedDict, List, Dict
from collections.abc import Callable
from nicegui import ui

from views.dashboard import DashboardView
from views.settings import SettingsView
from views.login import LoginView

from views.profile import ProfileView
from views.security import SecurityView

from views.report import ReportView
from views.statistics import StatisticsView

from views.home import HomeView



class TypedRoute(TypedDict):
    path: str
    label: str
    icon: str
    component: Callable[[], None]
    links: NotRequired[List[TypedRoute]] 




ROUTES: List[TypedRoute] = [
    {
        "path": "/",
        "label": "Home",
        "icon": "home",
        "component": HomeView,
        "links": [],
    },
    {
       
        "path": "/dashboard",
        "label": "Dashboard",
        "icon": "dashboard",
        "component": DashboardView,
        "links":  [
            {
                "path": "/report",
                "label": "Report",
                "icon": "report",
                "component": ReportView,
                "links": [],
            },
            {
                "path": "/statistics",
                "label": "Statistics",
                "icon": "statistics",
                "component": StatisticsView,
                "links": [],
            },

        ]
    },
    {
        "path": "/settings",
        "label": "Impostazioni",
        "icon": "settings",
        "component": SettingsView,
         "links": [
            {
                "path": "/profile",
                "label": "Profilo",
                "icon": "person",
                "component": ProfileView,
                "links": [],
            },
            {
                "path": "/secutity",
                "label": "Security",
                "icon": "security",
                "component": SecurityView,
                "links": [],
            },

        ],
    },
    {
        "path": "/login",
        "label": "Login",
        "icon": "login",
        "component": LoginView,
         "links": [],
    },
]


def get_flattened_routes(routes: List[TypedRoute]) -> Dict[str, Callable[[], None]]:
    flat: Dict[str, Callable[[], None]] = {}
    for r in routes:
        flat[r["path"]] = r["component"]
        if "links" in r and r["links"]:
            flat.update(get_flattened_routes(r["links"]))
    return flat




def main_btn_links(is_on_header: bool = False) -> List[ui.button]:
    btnList: List[ui.button] = []
    for route in ROUTES:
        btn = ui.button(
            route["label"],
            icon=route["icon"],
            on_click=lambda: ui.navigate.to(route["path"]),
        ).props("flat no-caps")
        btn.props("color=white") if is_on_header else btn.props("color=primary")
        btnList.append(btn)

    return btnList


def main_lnk_links(routes: List[TypedRoute]) -> List[ui.link]:
    lnkList: List[ui.link] = []
    for route in routes:
        if route["path"] != "/":
            lnk = ui.link(route["label"], route["path"]).classes(
                "px-6 py-3 text-blue-100 no-underline rounded hover:bg-blue-600 hover:underline hover:text-blue-200"
            )
                
            lnkList.append(lnk)

    # ui.notify(f"Links in main_lnk_links: {lnkList}")
    return lnkList
