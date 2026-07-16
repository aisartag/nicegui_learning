import logging

from nicegui import events, ui

from src.components.layout_events import user_state_modified
from src.core.setting_setup import SettingInit
from src.exceptions import UnAuthenticatedException
from src.routing.route_interfaces import PROTECTED_ROUTE_DEFAULT, SIGNIN
from src.services.user_service import UserService
from src.state.user_state import ProfileState, UserStateService

NAME = 'Profile'

settings = SettingInit()
logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


class UserProfileView:
	def __init__(self, profile_state: ProfileState):
		self.profile_state = profile_state

	def navigate_to_dashboard(self):
		ui.navigate.to(PROTECTED_ROUTE_DEFAULT)

	async def save_avatar(self, e: events.UploadEventArguments):
		"""
		Aggiorna la foto di profilo

		Args:
			e (events.UploadEventArguments): _description_

		Returns:
			_type_: _description_
		"""

		try:
			user_state = UserStateService.get_cached_state()
			if user_state is None or user_state.profile is None:
				raise UnAuthenticatedException('Utente non autenticato')

			user_id = user_state.id

			file_name = e.file.name
			file_bytes = await e.file.read()

			user_service = UserService()

			# aggiorna avatar_url su database
			new_avatar = await user_service.save_avatar(user_id, file_name, file_bytes)
			logger.info(f'new_avatar: {new_avatar}')

			# aggiorna user_state
			UserStateService.update_user_profile_avatar_url(new_avatar)

			# aggiorna avatar nell'image_display
			self.display_avatar.set_source(new_avatar)  # type: ignore
			# NiceGUI a bypass cache browser
			self.display_avatar.force_reload()
			self.upload_avatar.reset()

			# comunica ai sottoscrittori l'evento
			user_state_modified.emit()

		except ValueError as ex:
			ui.notify(f'Error: {ex}', type='negative')
			logger.error(ex)
			return
		except UnAuthenticatedException as ex:
			ui.notify(f'Error: {ex}', type='negative')
			logger.error(ex)
			return
		except Exception as ex:
			ui.notify(f'Error: {ex}', type='negative')
			logger.error(ex)
			return

	async def save_bio(self):

		try:
			user_state = UserStateService.get_cached_state()
			if user_state is None or user_state.profile is None:
				raise UnAuthenticatedException('Utente non autenticato')

			user_id = user_state.id

			user_service = UserService()

			# aggiorna avatar_url su database
			new_profile = await user_service.save_bio(user_id, self.bio_textarea.value)
			new_bio = new_profile.bio
			logger.info(f'new_bio: {new_bio}')

			# aggiorna  user_state
			UserStateService.update_user_profile_bio(new_bio)

			# comunica ai sottoscrittori l'evento *** non necessario **
			# user_state_modified.emit()

		except UnAuthenticatedException as ex:
			ui.notify(f'Error: {ex}', type='negative')
			logger.error(ex)
			return

		except Exception as ex:
			ui.notify(f'Error: {ex}', type='negative')
			logger.error(ex)
			return

	def image_avatar_render(self):
		self.display_avatar = ui.image(self.profile_state.avatar_url).classes(
			'w-36 h-36 rounded-full object-cover border-2 border-primary shadow-inner'
		)
		self.display_avatar.classes('w-36 h-36 rounded-full object-cover border-2 border-primary shadow-inner')
		if self.profile_state.avatar_url is not None:
			self.display_avatar.force_reload()

	def upload_avatar_render(self):

		self.upload_avatar = (
			ui.upload(
				label='Cambia foto',
				max_files=1,
				auto_upload=False,
				on_upload=self.save_avatar,
				on_rejected=lambda: ui.notify(
					'Tipo file non consentito.Estensioni consentite: .png, .jpg, .jpeg, .webp', type='negative'
				),
			)
			.props('accept=".png, .jpg, .jpeg, .webp"')
			.classes('w-full')
		)

	def bio_render(self):
		self.bio_textarea = (
			ui.textarea(
				label='Biografia / Presentazione',
				value=self.profile_state.bio,
				placeholder='Racconta qualcosa di te...',
			)
			.props('outlined clearable rows=10')
			.classes('w-full')
		)

		with ui.row().classes('w-full justify-between'):
			ui.button('Esci', on_click=self.navigate_to_dashboard).classes('w-1/4 btn-custom')
			ui.button('Salva', on_click=self.save_bio).classes('w-1/4 btn-custom')

	def render(self):
		with ui.card().classes('m-auto w-[60vw]  card-custom border-1 border-red-600'):
			with ui.row().classes('w-full justify-center items-center'):
				# ui.image(self.profile_state.avatar_url).classes(
				# 	'w-36 h-36 rounded-full object-cover border-2 border-primary shadow-inner'
				# )
				self.image_avatar_render()
			ui.separator().classes('w-full')

			with ui.card_section().classes('w-full gap-8 items-start  no-wrap grid grid-cols-1 lg:grid-cols-2 gap-8'):
				with ui.column().classes('w-full items-center'):
					ui.label('Foto Profilo').classes('text-sm font-semibold text-slate-500')

					self.upload_avatar_render()

				ui.separator().classes('lt-md w-full')

				with ui.column().classes('w-full items-center'):
					ui.label('Informazioni Personali').classes('text-sm font-semibold text-slate-500')
					self.bio_render()


async def ProfileView():

	logger.info(f'{NAME} avviata:{ui.context.client.id}')

	try:
		user_state = UserStateService.get_cached_state()
		logger.info(f'user_state: {user_state}')

		# controllo autenticazione: user_state può essere None UnAuthenticatedException
		if user_state is None:
			raise UnAuthenticatedException

		# controllo profile_state : profile_state non puo essere None e scatene
		profile_state = user_state.profile
		logger.info(f'profile_state: {profile_state}')

	except UnAuthenticatedException as e:
		logger.warning(e)
		ui.notify('Accesso negato. Effettua il login.', type='warning')
		ui.navigate.to(SIGNIN)
		return

	assert profile_state is not None
	view = UserProfileView(profile_state)
	view.render()
