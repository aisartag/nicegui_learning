import logging

from auth.schemas.login_schema import LoginSchema, get_clean_errors
from auth.services.auth_service import AuthService

# events import
from components.layout_events import loggedin_completed
from core.log_loader import configExtra
from database.engine import AsyncSessionLocal
from nicegui import PageArguments, ui
from pydantic import ValidationError
from routing.route_interfaces import PROTECTED_ROUTE_DEFAULT, SIGNUP

NAME = 'Login'

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


def LoginView(args: PageArguments):
	logger.info(f'{NAME} avviata:{ui.context.client.id}')

	with (
		ui.card()
		.props('bordered')
		.classes('mx-auto bg-slate-200 text-slate-800 dark:bg-slate-900  dark:text-blue-200')
		.style('max-width:480px; min-width:384px;')
	):
		with ui.card_section().classes('w-full'):
			with ui.row().classes('justify-center items-center text-2xl p-4'):
				with ui.column().classes('my-2 items-center'):
					ui.image('/static/images/e=mc2-1.png').classes('w-16 h-16')
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

					async with AsyncSessionLocal() as session:
						auth_service = AuthService(session)
						result = await auth_service.login(data.email, data.password)

					if not result:
						ui.notify('Login fallito', type='negative')
						return
					else:
						ui.notify('Login completato con successo!', type='positive')
						loggedin_completed.emit()

						ui.navigate.to(args.query_parameters.get('redirect_to', PROTECTED_ROUTE_DEFAULT))

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

		with ui.card_actions().classes('w-full gap-y-10'):
			ui.button('Login', on_click=on_submit).props('no-caps').classes(
				'w-full text-white bg-indigo-600! dark:bg-indigo-500!'
			)
			ui.link('Vai alla Home page', '/').classes(
				'no-underline text-sm text-blue-800 dark:text-blue-200 w-full text-right pr-1'
			)
