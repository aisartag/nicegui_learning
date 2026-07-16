import logging
from typing import Dict

from nicegui import PageArguments, ui
from pydantic import ValidationError

from src.auth.services.auth_service import AuthService
from src.components.layout_events import loggedin_completed
from src.core.setting_setup import SettingInit
from src.exceptions import InvalidCredentialsException
from src.routing.route_interfaces import PROTECTED_ROUTE_DEFAULT, SIGNUP
from src.schemas.login_schema import LoginSchema, get_clean_errors
from src.state.user_state import UserStateService

NAME = 'Login'

settings = SettingInit()
logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


class FormData:
	def __init__(self):
		self.email: str = ''
		self.password: str = ''


class UserLoginView:
	def __init__(self, args: PageArguments):
		self.args = args
		self.form_data = FormData()
		self.form_controls: Dict[str, ui.input] = {}

	async def on_submit(self):
		# 1. Resetta gli errori grafici precedenti
		for input_field in self.form_controls.values():
			input_field.props.pop('error', None)
			input_field.props.pop('error-message', None)
			input_field.update()

		try:
			data = LoginSchema(
				email=self.form_data.email,
				password=self.form_data.password,
			)

			auth_service = AuthService()
			user_orm = await auth_service.verify_credential(data.email, data.password)

			if user_orm:
				UserStateService.on_login(user_orm)

				ui.notify(f"Login effettuato. Benvenuto '{user_orm.username}'!")

				loggedin_completed.emit()

				ui.navigate.to(self.args.query_parameters.get('redirect_to', PROTECTED_ROUTE_DEFAULT))

			else:
				ui.notify('Login fallito', type='negative')
				return

		except ValidationError as e:
			# Errore di validazione Pydantic (Campi vuoti, email non valida, ecc.)
			friendly_errors = get_clean_errors(e)
			for field_name, error_msg in friendly_errors.items():
				if field_name in self.form_controls:
					self.form_controls[field_name].props['error'] = True
					self.form_controls[field_name].props['error-message'] = error_msg
					self.form_controls[field_name].update()
			ui.notify('Please fix the errors in the form.', type='negative')

		except InvalidCredentialsException as e:
			# Cattura l'errore di login, il database ha già fatto rollback autonomamente
			ui.notify(str(e), type='negative')
			logger.error(e)

		except Exception as e:
			ui.notify(f'Error: {e}', type='negative')
			logger.error(e)

	def render(self):
		logger.info(f'{NAME} render:{ui.context.client.id}')
		with (
			ui.card()
			.props('bordered')
			.classes('mx-auto bg-slate-200 text-blue-800 dark:bg-slate-900  dark:text-blue-200')
			.style('max-width:480px; min-width:384px;')
		):
			with ui.card_section().classes('w-full'):
				with ui.row().classes('justify-center items-center text-2xl p-4'):
					with ui.column().classes('my-2 items-center'):
						ui.image('/public/images/e=mc2-1.png').classes('w-16 h-16')
						ui.label('Entra nel tuo account')

				with ui.column().classes(
					'my-4'
				):  # .classes('justify-center items-center border-3 border-blue-600 p-4'):
					self.email_input = (ui.input('Email').props('outlined dense').classes('w-full')).bind_value(
						self.form_data, 'email'
					)  # props('icon="mail" clearable').classes('w-full')
					self.password_input = (
						ui.input('Password', password=True, password_toggle_button=True)
						.props('outlined dense')
						.classes('w-full')
					).bind_value(self.form_data, 'password')  # .props('icon="lock" clearable').classes('w-full')

				with ui.row().classes('justify-start items-center  p-2'):
					ui.label('Non hai un account?')
					ui.link('Registrati', SIGNUP).classes('no-underline text-blue-800 dark:text-blue-200')

			# with ui.card_actions().classes('w-full gap-y-8'):
			ui.button('Login', on_click=self.on_submit).props('no-caps').classes('w-full btn-indigo!')
			ui.link('Vai alla Home page', '/').classes(
				'no-underline text-sm text-blue-800 dark:text-blue-200 w-full text-right pr-1'
			)


def LoginView(args: PageArguments):
	logger.info(f'{NAME} avviata:{ui.context.client.id}')

	view = UserLoginView(args)
	view.render()
