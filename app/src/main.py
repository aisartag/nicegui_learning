import logging

from nicegui import app, ui

from src.components.layout_master import MasterLayout
from src.core.log_element_handler import ClientFilter, LogElementHandler
from src.core.setting_setup import SettingInit
from src.state.state_check import user_state_refresh
from src.state.user_state import UserStateService
from src.themes.global_styles import add_tailwind_styles

app.colors(
	primary='#5898d4',
	secondary='#26a69a',
	accent='#9c27b0',
	dark='#1d1d1d',
	dark_page='#121212',
	positive='#21ba45',
	negative='#c10015',
	info='#31ccec',
	warning='#f2c037',
)


formatter = logging.Formatter(
	fmt='%(asctime)s - %(levelname)s - %(name)s - %(lineno)d - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S',
)

settings = SettingInit()
logger = logging.getLogger(f'{settings.get_app_name()}.{__name__}')
root_logger = logging.getLogger(f'{settings.get_app_name()}')


async def root():

	logger.info(f'Inizio esecuzione root is authenticated? : {UserStateService.is_authenticated()}')

	await user_state_refresh()

	add_tailwind_styles()

	MasterLayout()

	# area log
	# with ui.expansion(value=True).classes("w-full h-full"):
	log_widget = ui.log(max_lines=100).classes('w-full h-40')
	handler = LogElementHandler(log_widget)
	handler.setFormatter(formatter)

	handler.addFilter(ClientFilter(ui.context.client.id))

	root_logger.addHandler(handler)
	ui.context.client.on_disconnect(lambda: logger.removeHandler(handler))  # type: ignore

	ui.button(
		'Log time',
		on_click=lambda: logger.warning(f'test log widget: {ui.context.client.id}'),
	)
