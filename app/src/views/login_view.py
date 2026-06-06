import logging

from auth.services.auth_service import AuthService
from components.layout_events import loggedin_completed
from core.log_loader import configExtra
from database.engine import AsyncSessionLocal
from exceptions import InvalidCredentialsException
from nicegui import PageArguments, app, ui
from pydantic import ValidationError
from routing.route_interfaces import PROTECTED_ROUTE_DEFAULT, SIGNUP
from schemas.login_schema import LoginSchema, get_clean_errors
from state.user_state import UserStorage

NAME = 'Login'

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


def LoginView(args: PageArguments):
	logger.info(f'{NAME} avviata:{ui.context.client.id}')

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

			with ui.column().classes('my-4'):  # .classes('justify-center items-center border-3 border-blue-600 p-4'):
				email_input = (
					ui.input('Email').props('outlined dense').classes('w-full')
				)  # props('icon="mail" clearable').classes('w-full')
				password_input = (
					ui.input('Password', password=True, password_toggle_button=True)
					.props('outlined dense')
					.classes('w-full')
				)  # .props('icon="lock" clearable').classes('w-full')

			with ui.row().classes('justify-start items-center  p-2'):
				ui.label('Non hai un account?')
				ui.link('Registrati', SIGNUP).classes('no-underline text-blue-800 dark:text-blue-200')

			all_inputs = {
				'email': email_input,
				'password': password_input,
			}

			async def on_submit():

				for input_field in all_inputs.values():
					input_field.props.pop('error', None)
					input_field.props.pop('error-message', None)
					input_field.update()

				try:
					data = LoginSchema(
						email=email_input.value or '',
						password=password_input.value or '',
					)

					async with AsyncSessionLocal.begin() as session:
						auth_service = AuthService(session)
						user_orm = await auth_service.verify_credential(data.email, data.password)

					if user_orm:
						app.storage.user['authenticated'] = True
						app.storage.user['user_id'] = user_orm.id
						app.storage.user['username'] = user_orm.username

						# attach UserStorage per session
						await UserStorage.login_user(user_orm)

						ui.notify(f"Login effettuato. Benvenuto '{user_orm.username}'!")

						loggedin_completed.emit()

						ui.navigate.to(args.query_parameters.get('redirect_to', PROTECTED_ROUTE_DEFAULT))

					else:
						ui.notify('Login fallito', type='negative')
						return

				except ValidationError as e:
					# ui.notify(f'Error: {e}', type='negative')
					logger.error(e.json())

					friendly_errors = get_clean_errors(e)

					# Correct way to apply dynamic props in NiceGUI:
					# Assign directly to the .props dict, then trigger .update()
					for field_name, error_msg in friendly_errors.items():
						if field_name in all_inputs:
							all_inputs[field_name].props['error'] = True
							all_inputs[field_name].props['error-message'] = error_msg
							all_inputs[field_name].update()

					ui.notify('Please fix the errors in the form.', type='negative')

				except InvalidCredentialsException as e:
					# Cattura l'errore di login, il database ha già fatto rollback autonomamente
					ui.notify(str(e), type='negative')
					logger.error(e)

				except Exception as e:
					ui.notify(f'Error: {e}', type='negative')
					logger.error(e)

		with ui.card_actions().classes('w-full gap-y-8'):
			ui.button('Login', on_click=on_submit).props('no-caps').classes('w-full btn-indigo!')
			ui.link('Vai alla Home page', '/').classes(
				'no-underline text-sm text-blue-800 dark:text-blue-200 w-full text-right pr-1'
			)
