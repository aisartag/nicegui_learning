import logging
from types import MappingProxyType
from typing import cast, get_args

from core.log_loader import configExtra
from nicegui import ui
from routing.route_childrens import ChildrenRegistry
from routing.route_events import childrens_emitted
from routing.route_interfaces import PATHS_ROOT, TypedRoutes
from views.dashboard_view import DashboardView
from views.home_view import HomeView
from views.login_view import LoginView
from views.settings_view import SettingsView

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


class MasterRoute:
    _ROUTES: TypedRoutes = {
        "/": {"label": "Home", "icon": "home", "component": HomeView, "childrens": []},
        "/dashboard": {
            "label": "Dashboard",
            "icon": "dashboard",
            "component": DashboardView,
            "childrens": ChildrenRegistry.DASHBOARD_CHILDREN,
        },
        "/settings": {
            "label": "Settings",
            "icon": "settings",
            "component": SettingsView,
            "childrens": ChildrenRegistry.SETTINGS_CHILDREN,
        },
        "/login": {
            "label": "Login",
            "icon": "login",
            "component": LoginView,
            "childrens": [],
        },
    }

    ROUTES = MappingProxyType(_ROUTES)

    @classmethod
    def setup(cls, path_initial: str):
        """
        Funzione di setup per la gestione delle rotte"""
        logger.info(f"setup in MasterRoutepath_initial: {path_initial}")
        cls.handle_path_change(cls.get_root_path(path_initial))

        # attiva listener per i cambiamenti di path
        ui.context.client.sub_pages_router.on_path_changed(
            lambda path: cls.handle_path_change(path)
        )

    @classmethod
    def handle_path_change(cls, path: str):
        """
        Funzione di callback per la gestione delle rotte"""
        logger.info(f"handle_path_change path: {path}")

        if path not in get_args(PATHS_ROOT):
            logger.info(f"handle_path_change: {path} non root")
            return

        childrens = cls.get_childrens_links(path)
        childrens_emitted.emit(childrens)

    @classmethod
    def get_route_details(cls, path: PATHS_ROOT):
        """Esempio di metodo di classe: usa 'cls' per accedere al dizionario"""
        return cls.ROUTES.get(path, "Route non trovata")

    @classmethod
    def as_nicegui_dict(cls):
        """Formatta i dati esattamente come li vuole ui.sub_pages"""
        data = {k: v["component"] for k, v in cls.ROUTES.items()}
        return data

    @classmethod
    def get_router_links(cls):
        selected_data = [
            {"path": path, "label": data["label"], "icon": data["icon"]}
            for path, data in cls.ROUTES.items()
        ]

        return selected_data

    @classmethod
    def get_childrens_links(cls, path: str) -> list[dict[str, str]] | None:
        if path in get_args(PATHS_ROOT):
            route = cls.ROUTES.get(cast(PATHS_ROOT, path), None)
            if route is not None:
                childrens = route.get("childrens", [])
                return [
                    {"path": path + child["path"], "label": child["label"]} for child in childrens
                ]
            else:
                return None

        else:
            return []

    @classmethod
    def get_root_path(cls, path: str) -> str:
        """
        restituisce la root path del path passato"""

        parts = path.strip("/").split("/")
        return f"/{parts[0]}" if parts[0] else "/"
