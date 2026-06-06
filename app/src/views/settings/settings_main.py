import logging

from core.log_loader import configExtra
from nicegui import ui

NAME = 'Settings Main'


logger = logging.getLogger(f'{configExtra["root_name"]}.{__name__}')


def SettingsMain():
	logger.info(f'{NAME}avviata:{ui.context.client.id}')
