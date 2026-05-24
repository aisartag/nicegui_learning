import logging

from auth.schemas.login_schema import LoginSchema, get_clean_errors
from auth.services.auth_service import AuthService
from core.log_loader import configExtra
from database.engine import AsyncSessionLocal
from nicegui import ui
from pydantic import ValidationError

NAME = 'Login'

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


def LoginView():
	logger.info(f'{NAME} avviata:{ui.context.client.id}')

	with ui.card().classes('mx-auto border-1 border-yellow-600').style('max-width:480px; min-width:384px;'):
		with ui.card_section().classes('w-full'):
			with ui.row().classes('justify-center items-center border-3 border-blue-600 p-4'):
				ui.label(NAME)

			with ui.column().classes('my-8'):  # .classes('justify-center items-center border-3 border-blue-600 p-4'):
				email_input = ui.input('Email').props('icon="mail" clearable').classes('w-full')
				password_input = ui.input('Password', password=True).props('icon="lock" clearable').classes('w-full')

			with ui.row().classes('justify-center items-center border-3 border-blue-600 p-4'):
				ui.label('Non hai un account?')
				ui.link('Registrati', '/register').classes('no-underline text-blue-800 dark:text-blue-200')

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

					async with AsyncSessionLocal() as session:
						auth_service = AuthService(session)
						result = await auth_service.login(data.email, data.password)

					if not result:
						ui.notify('Login fallito', type='negative')
						return
					else:
						ui.notify('Login completato!', type='positive')

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
				except Exception as e:
					ui.notify(f'Error: {e}', type='negative')
					logger.error(e)

		with ui.card_actions().classes('w-full'):
			ui.button('Submit', on_click=on_submit).classes('w-full')
