from collections.abc import Callable
from functools import partial
from typing import Any, List

from auth.services.login_state import get_logged_username, is_loggedin, logout
from components.select_theme import theme_choice
from nicegui import ui
from routing.route_master import MasterRoute
from themes.theme_manager import ThemeManager


class WidgetsLayout:
	def __init__(self):
		self.is_mobile = False

	def set_mobile(self, is_mobile: bool):
		self.is_mobile = is_mobile
		self.render_menu_for_childrens_as_buttons.refresh()

	@ui.refreshable_method
	def render_menu_master_as_buttons(self, callback: Callable[[], Any] | None = None):
		# 1. Definiamo la logica interna (helper)
		def _handle_click(path: str, cb: Callable[[], Any] | None):
			ui.navigate.to(path)
			if cb:
				cb()

		is_logged = is_loggedin()

		routes = MasterRoute.get_router_links()
		btnList: List[ui.button] = []

		for route in routes:
			if route['path'] == '/':
				continue

			guard = route['guard']
			should_show = False

			if guard == 'public':
				should_show = True
			elif guard == 'sign' and not is_logged:
				should_show = True
			elif guard == 'protected' and is_logged:
				should_show = True

			if should_show:
				# 2. Usiamo partial per collegare i dati specifici
				handler = partial(_handle_click, route['path'], callback)

				btn = (
					ui.button(route['label'], on_click=handler)
					.props('no-caps flat')
					.classes('px-4 py-2 font-bold text-lg text-blue-800 dark:text-blue-200')
				)
				btnList.append(btn)

		return btnList

	@ui.refreshable_method
	def render_user_zone(self) -> None:
		is_logged = is_loggedin()
		if is_logged:
			username = get_logged_username()

			with ui.row().classes('items-center'):
				ui.label(f'Benvenuto {username}').classes('text-lg')
				ui.button(icon='logout', on_click=logout).props('flat round ripple')

				with ui.row().classes('items-center gap-3 px-2'):
					# Un piccolo avatar testuale o icona
					with ui.avatar(color='primary', text_color='white').props('size=sm'):
						ui.label(username[0].upper())

					# Nome utente (invisibile su schermi molto piccoli se preferisci)
					ui.label(username).classes('font-medium text-sm text-slate-700 dark:text-blue-200 gt-xs')

					# Pulsante di Logout minimale con un'icona
					def _handle_logout():
						logout()
						ui.notify('Sessione chiusa con successo', type='info')

						# Rinfreschiamo ENTRAMBI i widget reattivi
						WidgetsLayout.render_menu_master_as_buttons.refresh()
						WidgetsLayout.render_user_zone.refresh()

						# Ritorniamo alla pagina di login
						ui.navigate.to('/login')

				ui.button(icon='logout', on_click=_handle_logout).props('round flat ripple dense').classes(
					'text-red-500 hover:text-red-700'
				).tooltip('Disconnetti')
		return None

	@ui.refreshable_method
	def render_menu_for_childrens_as_buttons(self, routes: List[dict[str, str]], callback: Callable[[], Any]):
		"""
		Renderizza i link dei figli della route corrente come pulsanti
		*** Il refresh viene rilanciato dall'interno nel metodo set_mobile(is_mobile)***
		"""

		# 1. Definiamo la logica interna (helper)
		def _handle_click(path: str, cb: Callable[[], Any]):
			ui.navigate.to(path)
			if self.is_mobile:
				cb()

		# routes = MasterRoute.get_router_links()
		btnList: List[ui.button] = []

		for route in routes:
			if route['path'] != '/':
				# 2. Usiamo partial per collegare i dati specifici
				handler = partial(_handle_click, route['path'], callback)

				btn = (
					ui.button(route['label'], on_click=handler)
					.props('no-caps flat')
					.classes('px-4 py-2 font-bold text-lg text-blue-800 dark:text-blue-200')
				)
				btnList.append(btn)

		return btnList

	def render_menu_as_dropdown(self, theme_manager: ThemeManager):
		"""
		Renderizza il menu con i link della route come dropdown"""
		# h-[calc(100vh-128px)]

		with ui.dialog().props('position=right backdrop-filter="blur(8px) brightness(40%)"') as dialog:
			with (
				ui.card()
				.classes(
					'absolute-right m-2 mr-1 !h-min-co  w-64 items-start bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200'
				)
				.style('height: 600px')
			):
				with ui.row().classes('w-full'):
					ui.button(icon='close', on_click=dialog.close).props('round flat ripple').classes('ml-auto')

				ui.separator().classes('w-full')

				with ui.column().classes('w-full'):
					self.render_menu_master_as_buttons(dialog.close)

				ui.separator().classes('w-full')

				with ui.row().classes('items-baseline'):
					ui.label('Theme:').classes('text-lg')
					theme_choice(theme_manager, dialog)

		ui.button(icon='more_vert', on_click=dialog.open).props('round flat ripple').classes(
			'lt-md text-blue-800 dark:text-blue-200'
		)
