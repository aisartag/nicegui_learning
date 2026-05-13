


from collections.abc import Callable
from typing import Dict, List, Literal, TypedDict


PATHS_ROOT = Literal["/", "/dashboard", "/settings", "/login"]
PATHS_CHILDRENS =Literal["/","/report", "/statistics", "/security", "/profile"]

class TypedRouteChildrenValue(TypedDict):
    path: PATHS_CHILDRENS
    label: str
    icon: str
    component: Callable[[], None]



class TypedRouteAttr(TypedDict):
    label: str
    icon: str
    component: Callable[[], None]
    childrens: List[TypedRouteChildrenValue]


TypedRoutes = Dict[PATHS_ROOT, TypedRouteAttr]
   