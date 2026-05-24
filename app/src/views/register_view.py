import logging

from core.log_loader import configExtra
from database.engine import AsyncSessionLocal
from nicegui import ui
from pydantic import ValidationError
from schemas.register_schema import RegisterSchema, get_clean_errors
from services.user_service import UserService

NAME = 'Register'

logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


def RegisterView():
	logger.info(f'{NAME} avviata:{ui.context.client.id}')

	# with ui.column().classes('w-full  border-3 border-bg-yellow-600'):
	# with ui.row().classes('w-full mx-auto border-2 border-red-600'):
	with ui.card().classes('mx-auto border-1 border-yellow-600').style('max-width:480px; min-width:384px;'):
		with ui.card_section().classes('w-full'):
			with ui.row().classes('justify-center items-center border-3 border-blue-600 p-4'):
				ui.label(NAME)

			with ui.column().classes('my-8'):  # .classes('justify-center items-center border-3 border-blue-600 p-4'):
				username_input = ui.input('Username', value='').props('clearable').classes('w-full')
				with username_input.add_slot('append'):
					ui.icon('person').props('color=primary')

				email_input = ui.input('Email').props('clearable').classes('w-full')
				with email_input.add_slot('append'):
					ui.icon('mail').props('color=primary')

				password_input = ui.input('Password', password=True).props('clearable').classes('w-full')
				with password_input.add_slot('append'):
					ui.icon('lock').props('color=primary')

				confirm_password_input = (
					ui.input('Confirm Password', password=True).props('clearable').classes('w-full')
				)
				with confirm_password_input.add_slot('append'):
					ui.icon('lock').props('color=primary')

			all_inputs = {
				'username': username_input,
				'email': email_input,
				'password': password_input,
				'confirm_password': confirm_password_input,
			}

			async def on_submit():

				for input_field in all_inputs.values():
					input_field.props.pop('error', None)
					input_field.props.pop('error-message', None)
					input_field.update()

				try:
					data = RegisterSchema(
						username=username_input.value or '',
						email=email_input.value or '',
						password=password_input.value or '',
						confirm_password=confirm_password_input.value or '',
					)

					try:
						async with AsyncSessionLocal() as session:
							user_service = UserService(session)
							await user_service.register_user_with_profile(data.username, data.email, data.password)

						ui.notify('Registration completed!', type='positive')
						ui.navigate.to('/login')

					except Exception as e:
						ui.notify(f'Error: {e}', type='negative')
						logger.error(e)

					# if not result:
					# 	ui.notify('Login fallito', type='negative')
					# 	return
					# else:
					# 	ui.notify('Login completato!', type='positive')

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
