import logging
from collections.abc import Callable
from functools import partial
from typing import Any, List

from auth.services.auth_state import AuthState
from components.select_theme import theme_choice
from components.user_avater import UserAvatar
from core.log_loader import configExtra
from nicegui import ui
from routing.route_interfaces import MENU_MASTER_EXCLUDE, SIGNIN  # , SIGNIN
from routing.route_master import MasterRoute
from state.user_state import UserStorage
from themes.theme_manager import ThemeManager

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


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

		is_logged = AuthState.is_authenticated()

		routes = MasterRoute.get_router_links()
		btnList: List[ui.button] = []

		for route in routes:
			if route['path'] in MENU_MASTER_EXCLUDE:
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
					.classes('px-4 py-2 font-bold text-sm text-blue-800 dark:text-blue-200')
				)
				btnList.append(btn)

	@ui.refreshable_method
	def render_user_zone(self):

		def _navigate_to_login():
			ui.navigate.to(SIGNIN)
			menu.close()

		def _handle_logout():

			# reset cookie e user state
			AuthState.logout()

			ui.notify('Sessione chiusa con successo', type='info')

			# Rinfreschiamo ENTRAMBI i widget reattivi
			self.render_menu_master_as_buttons.refresh()
			self.render_user_zone.refresh()

			# Ritorniamo alla pagina di login
			ui.navigate.to(SIGNIN)
			return

		user_state = UserStorage.get_user_state()
		logger.info(f'user_state: {user_state}')

		# layout_controls = LayoutControls()
		with ui.element('div').classes('relative flex items-center justify-end'):
			avatar_display = UserAvatar('sm', user_state).classes('cursor-pointer')

			with ui.menu().props('auto-close').classes('w-48') as menu:
				menu.props('anchor="bottom right" self="top right" :offset="[0, 8]"')

				with ui.column().classes(
					'items-center p-3 rounded-md mb-2 bg-slate-100 text-slate-800 dark:bg-slate-800  dark:text-blue-200'
				):
					UserAvatar('xl', user_state).classes('mb-1 btn-indigo')
					if user_state:
						ui.label(user_state.username).classes('font-bold text-blue-600 dark:text-blue-200 text-lg')
					else:
						with ui.row().classes('w-full items-center justify-center'):
							ui.button('Accedi', on_click=_navigate_to_login).props('no-caps rounded').classes(
								'text-white bg-indigo-600! dark:bg-indigo-500!'
							)
						return

				if user_state:
					# Opzioni per utente loggato
					ui.item('Il mio Profilo', on_click=lambda: ui.navigate.to('/profile')).props('v-close-popup')
					# ui.item('Impostazioni', on_click=lambda: ui.notify('Apri impostazioni...')).props('v-close-popup')
					ui.separator()
					ui.item('Logout', on_click=_handle_logout).props('v-close-popup').classes('text-red')
				# else:
				# 	# Opzioni per utente anonimo
				# 	ui.item('Accedi / Login', on_click=lambda: ui.notify('Apri schermata login...')).props(
				# 		'v-close-popup'
				# 	)
				# 	ui.item('Registrati', on_click=lambda: ui.notify('Apri registrazione...')).props('v-close-popup')

			avatar_display.on('click', menu.open)

			# with (
			# 	ui.menu()
			# 	.props('auto-close')
			# 	.classes('w-64 p-2 bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200') as menu
			# ):
			# 	with ui.column().classes(
			# 		'items-center p-3 rounded-md mb-2 bg-slate-100 text-slate-800 dark:bg-slate-800  dark:text-blue-200'
			# 	):
			# 		with ui.avatar(size='lg').classes(
			# 			'mb-1 text-white bg-indigo-600! dark:bg-indigo-500!'
			# 		):  # .style(f'background-image: url({utente_corrente["avatar_url"]}); background-size: cover;')
			# 			ui.label(user_image)

			# 		ui.label(user).classes('font-bold text-blue-600 dark:text-blue-200 text-lg')

			# 		if not UserStateManager.is_authenticated():
			# 			with ui.row().classes('w-full items-center justify-center'):
			# 				ui.button('Accedi', on_click=_navigate_to_login).props('no-caps rounded').classes(
			# 					'text-white bg-indigo-600! dark:bg-indigo-500!'
			# 				)
			# 			return

			# 	ui.menu_item('Profilo', on_click=lambda: ui.navigate.to('/profile'))

			# 	ui.separator()

			# 	ui.menu_item('Logout', on_click=_handle_logout)

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

	def render_menu_as_dropdown(self, theme_manager: ThemeManager):
		with (
			ui.button(
				icon='more_vert',
			)
			.props('round flat ripple')
			.classes('text-blue-800 dark:text-blue-200')
		):
			with (
				ui.menu()
				# .props('auto-close')
				.classes('w-72 p-4 bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200') as menu
			):
				with ui.row().classes('w-full'):
					# ui.button(icon='close', on_click=menu.close).props('round flat ripple').classes('ml-auto')

					# ui.separator().classes('w-full')

					with ui.column().classes('w-full'):
						self.render_menu_master_as_buttons(menu.close)

					ui.separator().classes('w-full')

					with ui.row().classes('items-baseline'):
						ui.label('Dark mode:').classes('text-lg')
						theme_choice(theme_manager, menu)
