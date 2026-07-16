import logging
from typing import Dict

from nicegui import ui
from pydantic import ValidationError

from src.core.setting_setup import SettingInit
from src.exceptions import RegistrationException
from src.routing.route_interfaces import SIGNIN
from src.schemas.register_schema import RegisterSchema, get_clean_errors
from src.services.user_service import UserService

NAME = 'Register'

settings = SettingInit()
logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


class FormData:
	def __init__(self):
		self.username: str = ''
		self.email: str = ''
		self.password: str = ''
		self.confirm_password: str = ''


class UserRegisterView:
	def __init__(self):
		self.form_data = FormData()
		self.form_controls: Dict[str, ui.input] = {}

	async def on_submit(self):
		# 1. Resetta gli errori grafici precedenti
		for input_field in self.form_controls.values():
			input_field.props.pop('error', None)
			input_field.props.pop('error-message', None)
			input_field.update()

		try:
			# Validazione Pydantic
			data = RegisterSchema(
				username=self.form_data.username,
				email=self.form_data.email,
				password=self.form_data.password,
				confirm_password=self.form_data.confirm_password,
			)

			logger.info(f'Validazione Pydantic: {data}')

			user_service = UserService()
			await user_service.register_user_with_profile(
				username=data.username, email=data.email, clear_password=data.password
			)

			ui.notify('Registration completed!', type='positive')
			ui.navigate.to(SIGNIN)

		except ValidationError as e:
			# Errore di validazione Pydantic (Campi vuoti, email non valida, ecc.)
			friendly_errors = get_clean_errors(e)
			for field_name, error_msg in friendly_errors.items():
				if field_name in self.form_controls:
					self.form_controls[field_name].props['error'] = True
					self.form_controls[field_name].props['error-message'] = error_msg
					self.form_controls[field_name].update()
			ui.notify('Please fix the errors in the form.', type='negative')

		except ValueError as e:
			# Errore di validazione logica lanciato dal Service (es: "Email già in uso")
			# Nota: se nel Service lanci ValueError per duplicati, lo catturi qui!
			ui.notify(str(e), type='negative')
			logger.warning(f'Validazione fallita: {e}')

		except RegistrationException as e:
			# Errore specifico del Database / Transazione fallita
			ui.notify(f'Registration Error: {e}', type='negative')
			logger.error(f'Errore registrazione: {e}')

		except Exception as e:
			# Qualsiasi altro errore imprevisto (es. crash di rete, errore di sintassi, ecc.)
			ui.notify('An unexpected error occurred. Please try again.', type='negative')
			logger.error(f'Errore imprevisto nel submit: {e}', exc_info=True)

	def render(self):
		logger.info(f'{NAME} render:{ui.context.client.id}')
		with (
			ui.card()
			.classes('mx-auto bg-slate-100 text-slate-800 dark:bg-slate-900  dark:text-blue-200')
			.style('max-width:480px; min-width:384px;')
		):
			with ui.card_section().classes('w-full'):
				with ui.row().classes('justify-center items-center text-2xl p-4'):
					with ui.column().classes('my-2 items-center'):
						ui.image('/public/images/e=mc2-1.png').classes('w-16 h-16')
						ui.label('Registrazione account')

				with ui.column().classes(
					'my-4'
				):  # .classes('justify-center items-center border-3 border-blue-600 p-4'):
					self.username_input = (ui.input('Username').props('outlined dense').classes('w-full')).bind_value(
						self.form_data, 'username'
					)  # props('clearable')
					# with username_input.add_slot('append'):
					# 	ui.icon('person').props('color=primary')

					self.form_controls['username'] = self.username_input

					self.email_input = (ui.input('Email').props('outlined dense').classes('w-full')).bind_value(
						self.form_data, 'email'
					)  # props('clearable').classes('w-full')
					# with email_input.add_slot('append'):
					# 	ui.icon('mail').props('color=primary')

					self.form_controls['email'] = self.email_input

					self.password_input = (
						ui.input('Password', password=True, password_toggle_button=True)
						.props('outlined dense')
						.classes('w-full')
					).bind_value(self.form_data, 'password')  # props('clearable').classes('w-full')
					# with password_input.add_slot('append'):
					# 	ui.icon('lock').props('color=primary')

					self.form_controls['password'] = self.password_input

					self.confirm_password_input = (
						ui.input('Confirm Password', password=True, password_toggle_button=True)
						.props('outlined dense')
						.classes('w-full')  # props('clearable').classes('w-full')
					).bind_value(self.form_data, 'confirm_password')

					self.form_controls['confirm_password'] = self.confirm_password_input

			with ui.card_actions().classes('w-full gap-y-8'):
				ui.button('Registrati', on_click=self.on_submit).props('no-caps').classes(
					'w-full text-white bg-indigo-600! dark:bg-indigo-500!'
				)
				ui.link('Vai alla Home page', '/').classes(
					'no-underline text-sm text-blue-800 dark:text-blue-200 w-full text-right pr-1'
				)


def RegisterView():
	# logger.info(f'{NAME} avviata:{ui.context.client.id}')

	view = UserRegisterView()
	view.render()
