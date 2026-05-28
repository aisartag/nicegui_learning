from collections.abc import Callable
from functools import partial
from typing import Any, List

from auth.services.login_state import get_logged_username, is_loggedin, logout
from components.select_theme import theme_choice
from nicegui import ui
from routing.route_interfaces import SIGNIN
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

	# @ui.refreshable_method
	# def render_user_zone(self) -> None:
	# 	is_logged = is_loggedin()
	# 	if is_logged:
	# 		username = get_logged_username()

	# 		with ui.row().classes('items-center'):
	# 			ui.label(f'Benvenuto {username}').classes('text-lg')
	# 			ui.button(icon='logout', on_click=logout).props('flat round ripple')

	# 			with ui.row().classes('items-center gap-3 px-2'):
	# 				# Un piccolo avatar testuale o icona
	# 				with ui.avatar(color='primary', text_color='white').props('size=sm'):
	# 					ui.label(username[0].upper())

	# 				# Nome utente (invisibile su schermi molto piccoli se preferisci)
	# 				ui.label(username).classes('font-medium text-sm text-slate-700 dark:text-blue-200 gt-xs')

	# 				# Pulsante di Logout minimale con un'icona
	# 				def _handle_logout():
	# 					logout()
	# 					ui.notify('Sessione chiusa con successo', type='info')

	# 					# Rinfreschiamo ENTRAMBI i widget reattivi
	# 					self.render_menu_master_as_buttons.refresh()
	# 					self.render_user_zone.refresh()

	# 					# Ritorniamo alla pagina di login
	# 					# ui.navigate.to('/login')

	# 			ui.button(icon='logout', on_click=_handle_logout).props('round flat ripple dense').classes(
	# 				'text-red-500 hover:text-red-700'
	# 			).tooltip('Disconnetti')
	# 	return None

	@ui.refreshable_method
	def render_user_zone(self):
		is_logged = is_loggedin()
		if is_logged:
			user = get_logged_username()
			user_image = user[0].upper()
		else:
			user = 'Accedi a nicegui_learning'
			user_image = '?'

		def _navigate_to_login():
			ui.navigate.to(SIGNIN)
			menu.close()

		def _handle_logout():

			logout()
			ui.notify('Sessione chiusa con successo', type='info')

			# Rinfreschiamo ENTRAMBI i widget reattivi
			self.render_menu_master_as_buttons.refresh()
			self.render_user_zone.refresh()

			# Ritorniamo alla pagina di login
			ui.navigate.to(SIGNIN)

		with ui.avatar(size='sm').classes('cursor-pointer shadow-md text-white bg-indigo-600! dark:bg-indigo-500!'):
			ui.label(user_image)  # .classes('dark:text-blue-200')
			# ui.image(utente_corrente["avatar_url"])

			with (
				ui.menu()
				.props('auto-close')
				.classes('w-64 p-2 bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200') as menu
			):
				with ui.column().classes(
					'items-center p-3 rounded-md mb-2 bg-slate-100 text-slate-800 dark:bg-slate-800  dark:text-blue-200'
				):
					with ui.avatar(size='lg').classes(
						'mb-1 text-white bg-indigo-600! dark:bg-indigo-500!'
					):  # .style(f'background-image: url({utente_corrente["avatar_url"]}); background-size: cover;')
						ui.label(user_image)

					ui.label(user).classes('font-bold text-blue-600 dark:text-blue-200 text-lg')

					if not is_logged:
						with ui.row().classes('w-full items-center justify-center'):
							ui.button('Accedi', on_click=_navigate_to_login).props('no-caps rounded').classes(
								'text-white bg-indigo-600! dark:bg-indigo-500!'
							)
						return

				ui.menu_item('Profilo', on_click=lambda: ui.navigate.to('/profile'))

				ui.separator()

				ui.menu_item('Logout', on_click=_handle_logout)

	# def render_user_zone_minimal(self):
	# 	def go_to_profile():
	# 		ui.notify('Reindirizzamento alla pagina del profilo...')

	# 	def do_logout():
	# 		ui.notify('Logout effettuato con successo!')

	# 	with ui.row().classes('items-center cursor-pointer'):
	# 		is_logged = is_loggedin()
	# 		if is_logged:
	# 			initial_user = get_logged_username()[0].upper()
	# 		else:
	# 			initial_user = '?'

	# 		with ui.avatar(color='primary', text_color='white').props('size=sm'):
	# 			ui.label(initial_user)

	# 		with ui.menu().props('auto-close'):
	# 			ui.menu_item('Profilo', on_click=go_to_profile)  # , icon="account_circle"
	# 			ui.separator()
	# 			ui.menu_item('Logout', on_click=do_logout)  # , icon="logout"

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

	def render_menu_as_dialog(self, theme_manager: ThemeManager):
		"""
		Renderizza il menu con i link della route come dialog"""
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
			'text-blue-800 dark:text-blue-200'
		)
