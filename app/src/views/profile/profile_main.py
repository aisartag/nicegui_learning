import logging

from nicegui import ui
from src.core.setting_setup import SettingInit

NAME = 'Profile Main'

settings = SettingInit()
logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')


def ProfileMain():
	logger.info(f'{NAME}avviata:{ui.context.client.id}')
