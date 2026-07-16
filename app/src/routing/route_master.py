import logging
from collections.abc import Callable
from types import MappingProxyType
from typing import cast, get_args

from nicegui import ui

from src.core.setting_setup import SettingInit
from src.routing.route_childrens import ChildrenRegistry
from src.routing.route_interfaces import PATHS_ROOT, TypedRouteAttr, TypedRoutes
from src.state.user_state import UserStateService
from src.views.dashboard_view import DashboardView
from src.views.home_view import HomeView
from src.views.login_view import LoginView
from src.views.profile_view import ProfileView
from src.views.register_view import RegisterView
from src.views.settings_view import SettingsView

settings = SettingInit()

logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


class MasterRoute:
	_ROUTES: TypedRoutes = {
		'/': {'label': 'Home', 'icon': 'home', 'component': HomeView, 'childrens': [], 'guard': 'public'},
		'/dashboard': {
			'label': 'Dashboard',
			'icon': 'dashboard',
			'component': DashboardView,
			'childrens': ChildrenRegistry.DASHBOARD_CHILDREN,
			'guard': 'protected',
		},
		'/settings': {
			'label': 'Settings',
			'icon': 'settings',
			'component': SettingsView,
			'childrens': ChildrenRegistry.SETTINGS_CHILDREN,
			'guard': 'protected',
		},
		'/login': {'label': 'Login', 'icon': 'login', 'component': LoginView, 'childrens': [], 'guard': 'sign'},
		'/register': {
			'label': 'Register',
			'icon': 'register',
			'component': RegisterView,
			'childrens': [],
			'guard': 'sign',
		},
		'/profile': {
			'label': 'Profile',
			'icon': 'profile',
			'component': ProfileView,
			'childrens': [],  # ChildrenRegistry.PROFILE_CHILDREN,
			'guard': 'protected',
		},
	}
	ROUTES = MappingProxyType(_ROUTES)

	def __init__(
		self,
		on_sign_layout: Callable[[bool], None],
		on_childrens_changed: Callable[[list[dict[str, str]] | None], None],
	) -> None:
		"""
		Inizializzazione per istanza (1 per ogni Client/Tab aperto).
		Riceve le callback per aggiornare direttamente la UI del Layout specifico.
		"""
		self.on_sign_layout = on_sign_layout
		self.on_childrens_changed = on_childrens_changed

	def start(self, path_initial: str) -> None:
		"""Attiva il sistema di routing per il client corrente."""
		# Primo avvio basato sul path di caricamento
		root_path = self.get_root_path(path_initial)
		self.handle_path_change(root_path)

		# Registriamo l'evento sul router del client attuale. NiceGUI passa un oggetto evento 'e'
		# Usiamo una lambda che invoca l'istanza corretta evitando sovrascritture tra utenti
		ui.context.client.sub_pages_router.on_path_changed(lambda path: self.handle_path_change(path))

	def handle_path_change(self, path: str):

		logger.info(f'handle_path_change path: {path}')

		# Controllo Type-Safe: Pyright riconosce il tipo grazie al pattern di guardia
		valid_paths = get_args(PATHS_ROOT)
		if path not in valid_paths:
			logger.info(f'handle_path_change: {path} non root')
			return

		# Da qui in poi, per Pyright 'path' è un membro valido di PATHS_ROOT
		# Usiamo il dizionario in modo diretto e type-safe senza cast artificiali
		route: TypedRouteAttr = self.ROUTES[cast(PATHS_ROOT, path)]

		guard = route.get('guard')

		# Inibisce se loggedin di navigare su pagine con guard='sign'
		if guard == 'sign' and UserStateService.is_authenticated():
			ui.navigate.to('/')  # home
			return

		# per nscondere la barra di navigazione per rotte 'sign
		self.on_sign_layout(not guard == 'sign')

		if guard == 'protected' and not UserStateService.is_authenticated():
			logger.info(f'Accesso negato. Salvo il redirect per: {path}')
			# Passiamo il path originale (completo di eventuali sotto-pagine) nell'URL
			self.on_sign_layout(False)
			ui.navigate.to(f'/login?redirect_to={path}')
			return

		# Gestione Sotto-Menu (Invio diretto alla callback del layout)
		childrens = self.get_childrens_links(cast(PATHS_ROOT, path))
		self.on_childrens_changed(childrens)

	@classmethod
	def get_route_details(cls, path: PATHS_ROOT):
		"""Esempio di metodo di classe: usa 'cls' per accedere al dizionario"""
		return cls.ROUTES.get(path)

	@classmethod
	def get_router_links(cls):
		selected_data = [
			{'path': path, 'label': data['label'], 'icon': data['icon'], 'guard': data['guard']}
			for path, data in cls.ROUTES.items()
		]

		return selected_data

	def get_childrens_links(self, path: PATHS_ROOT) -> list[dict[str, str]] | None:

		route = self.ROUTES.get(path)
		if route is None:
			return None

		childrens = route.get('childrens', [])
		return [{'path': path + child['path'], 'label': child['label']} for child in childrens]

	@classmethod
	def as_nicegui_dict(cls):
		return {k: v['component'] for k, v in cls.ROUTES.items()}

	@classmethod
	def get_root_path(cls, path: str) -> PATHS_ROOT:
		parts = path.strip('/').split('/')
		root = f'/{parts[0]}' if parts[0] else '/'
		if root in get_args(PATHS_ROOT):
			return cast(PATHS_ROOT, root)
		return '/'
