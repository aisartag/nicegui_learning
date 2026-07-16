from nicegui import ui

from src.state.user_state import UserState


class UserAvatar(ui.avatar):
	def __init__(self, size: str, user_state: UserState | None = None):
		self.user_state: UserState | None = user_state
		self.size = size

		# Se l'utente NON è loggato, usiamo l'icona nativa 'person'
		icon = 'person' if not self.user_state else None
		super().__init__(icon, color='primary', text_color='white', size=self.size)

		username = self.user_state.username if self.user_state else None
		avatar = self.user_state.profile.avatar_url if self.user_state and self.user_state.profile else None
		if username:
			with self:
				if avatar:
					img = ui.image(f'{avatar}').classes('w-full h-full  object-cover')
					img.force_reload()
				else:
					initials = ''.join([part[0].upper() for part in username.split() if part])[:2]
					ui.label(initials)
