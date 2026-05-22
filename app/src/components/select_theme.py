from typing import cast, get_args

from nicegui import ui, events
from themes.theme_manager import ThemeLiteral, ThemeManager
#  from typing import TypeVar, Any

import logging
from core.log_loader import configExtra

logger = logging.getLogger(f"{configExtra['root_name']}.{__name__}")


def theme_choice(manager: ThemeManager, container: ui.dialog | None = None):
    logger.info(f"theme_choice avviato: {ui.context.client.id}")
    options = {
        "light": {"label": "Chiaro", "icon": "light_mode"},
        "dark": {"label": "Scuro", "icon": "dark_mode"},
        "auto": {"label": "Automatico", "icon": "settings_brightness"},
    }

    def update_mode(e: events.ValueChangeEventArguments[str]) -> None:
        # Qui Pyright valida che e.value sia compatibile con ModeType

        if e.value in get_args(ThemeLiteral):
            manager.mode = cast(ThemeLiteral, e.value)  # Errore se e.value
            container.close() if container else None
        else:
            ui.notify(f"{e.value} non previsto")

    # Options as a list of strings
    select = ui.select(
        options=options, value=manager.mode, on_change=update_mode
    ).classes("w-32")

    select.add_slot(
        "option",
        """
        <q-item v-bind="props.itemProps">
            <q-item-section avatar>
                <q-icon :name="props.opt.label.icon"></q-icon>
            </q-item-section>
            <q-item-section>
                <span>{{props.opt.label.label}}</span>
            </q-item-section>
        </q-item>
    """,
    )

    select.add_slot(
        "selected-item",
        """
        <div class="row items-center no-wrap">
            <q-icon :name="props.opt.label.icon" size="sm" class="q-mr-sm"></q-icon>
            <span class="ellipsis">{{ props.opt.label.label }}</span>
        </div>
    """,
    )
