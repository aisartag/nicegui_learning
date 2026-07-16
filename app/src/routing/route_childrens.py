from typing import List

from typing_extensions import Literal

from src.routing.route_interfaces import TypedRouteChildrenValue
from src.views.dashboard_main import DashboardMain
from src.views.profile.avatar_view import AvatarView
from src.views.profile.bio_view import BioView
from src.views.profile.profile_main import ProfileMain
from src.views.report_view import ReportView
from src.views.settings.security_view import SecurityView
from src.views.settings.settings_main import SettingsMain
from src.views.settings.typology_view import TypologyView
from src.views.statistics_view import StatisticsView

PARENT_CHILDREN = Literal[
	'DASHBOARD_CHILDREN', 'SETTINGS_CHILDREN', 'PROFILE_CHILDREN'
]  # = ChildrenRegistry.DASHBOARD_CHILDREN, ChildrenRegistry.SETTINGS_CHILDREN


class ChildrenRegistry:
	DASHBOARD_CHILDREN: List[TypedRouteChildrenValue] = [
		{
			'path': '/',
			'label': 'Dashboard Main',
			'icon': '',
			'component': DashboardMain,
		},
		{
			'path': '/report',
			'label': 'Report',
			'icon': 'report',
			'component': ReportView,
		},
		{
			'path': '/statistics',
			'label': 'Statistics',
			'icon': 'statistics',
			'component': StatisticsView,
		},
	]

	SETTINGS_CHILDREN: List[TypedRouteChildrenValue] = [
		{
			'path': '/',
			'label': 'SettingsMain',
			'icon': '',
			'component': SettingsMain,
		},
		{
			'path': '/security',
			'label': 'Security',
			'icon': 'security',
			'component': SecurityView,
		},
		{
			'path': '/typology',
			'label': 'Typology',
			'icon': '',
			'component': TypologyView,
		},
	]

	PROFILE_CHILDREN: List[TypedRouteChildrenValue] = [
		{
			'path': '/',
			'label': 'ProfileMain',
			'icon': '',
			'component': ProfileMain,
		},
		{
			'path': '/bio',
			'label': 'Bio',
			'icon': '',
			'component': BioView,
		},
		{
			'path': '/avatar',
			'label': 'Avatar',
			'icon': '',
			'component': AvatarView,
		},
	]

	@classmethod
	def as_nicegui_dict(cls, section: PARENT_CHILDREN):
		"""Formatta i dati esattamente come li vuole ui.sub_pages"""
		data = getattr(cls, section, [])
		return {item['path']: item['component'] for item in data}

	@classmethod
	def get_childrens_list(cls):
		"""Formatta i dati esattamente come li vuole ui.sub_pages"""
		attributi = [a for a in dir(cls) if not callable(getattr(cls, a)) and not a.startswith('__')]
		return attributi
