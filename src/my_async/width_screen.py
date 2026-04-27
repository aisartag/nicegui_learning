from nicegui import ui
from typing import cast
import asyncio
async def async_get_width() -> int:
    w = cast(int, await ui.run_javascript('window.innerWidth'))  
    ui.notify(f'width screen async: {w}')
    return w


def get_width():
    w = asyncio.run(async_get_width())
    ui.notify(f'width screen sync: {w}')




ui.button('width screen', on_click=get_width)





ui.run() # type: ignore