from collections.abc import Callable
from typing import Any, Dict, List, Literal, TypedDict

PATHS_ROOT = Literal['/', '/dashboard', '/settings', '/login', '/register', '/profile']
PATHS_CHILDRENS = Literal['/', '/report', '/statistics', '/security', '/typology', '/bio', '/avatar']


GUARD_LEVEL = Literal['protected', 'public', 'sign']

PROTECTED_ROUTE_DEFAULT: PATHS_ROOT = '/dashboard'
PUBLIC_ROUTE_DEFAULT: PATHS_ROOT = '/'
SIGNUP = '/register'
SIGNIN = '/login'
MENU_MASTER_EXCLUDE: List[PATHS_ROOT] = ['/', '/profile']


class TypedRouteChildrenValue(TypedDict):
	path: PATHS_CHILDRENS
	label: str
	icon: str
	component: Callable[[], None]


class TypedRouteAttr(TypedDict):
	label: str
	icon: str
	component: Callable[..., Any]
	childrens: List[TypedRouteChildrenValue]
	guard: GUARD_LEVEL


TypedRoutes = Dict[PATHS_ROOT, TypedRouteAttr]
