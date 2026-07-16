import logging

from nicegui import ui

from src.core.setting_setup import SettingInit
from src.routing.route_interfaces import SIGNIN
from src.services.user_service import UserService
from src.state.user_state import UserStateService

settings = SettingInit()

logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


async def user_state_refresh():
	user_id = UserStateService.get_user_id()
	logger.info(f'user_id: {user_id}')

	if user_id is not None:
		user_orm = None
		userService = UserService()
		user_orm = await userService.get_user_with_profile(user_id)

		if user_orm is None:
			UserStateService.on_logout()
			ui.notify('Sessione non valida o utente non trovato nel sistema.', type='negative')
			logger.warning('Sessione non valida o utente non trovato nel sistema.')

			# Ritorniamo alla pagina di login
			ui.navigate.to(SIGNIN)

		else:
			UserStateService.on_login(user_orm)
