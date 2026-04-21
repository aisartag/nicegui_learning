import sys
from pathlib import Path
from nicegui import ui, app
import logging


# Aggiunge la cartella 'src' al percorso di ricerca di Python
# ovvero il sys.path.insert(0....) 0 in testa
src_path = str(Path(__file__).parent / "src")
if src_path not in sys.path:
    sys.path.insert(0, src_path)

from core.config import configuration
from core.boot import bootstrap
from themes.theme_manager import ThemeManager

# Se il bootstrap fallisce, l'app non deve nemmeno provare a partire
if not bootstrap():
    sys.exit(1)

print(f"{configuration['appName']}.{__name__}")


# Esempio di utilizzo nella pagina
# @ui.page("/")
def root():

    ui.notify(f"{configuration['appName']}.{__name__}", position="top-right")
    logger = logging.getLogger(f"{configuration['appName']}.test")
    logger.info("test theme manager avviato")

    # Passiamo app.storage.user (che è un PersistentDict)

    manager = ThemeManager(app.storage.user)

    options = {
        "light": {"label": "Chiaro", "icon": "light_mode"},
        "dark": {"label": "Scuro", "icon": "dark_mode"},
        "auto": {"label": "Automatico", "icon": "settings_brightness"},
    }

    with ui.card().classes("w-64 p-4 items-center mx-auto"):
        with ui.row().classes("items-center p-4"):
            ui.select(["light", "dark", "auto"], label="Tema").bind_value(
                manager, "mode"
            ).classes("w-40")

        with ui.row().classes("items-center p-4"):
            ui.label("Cambia tema:")

            # Il bottone si aggiorna da solo grazie a bind_icon_from
            ui.button(on_click=manager.cycle).props("round flat").bind_icon_from(
                manager, "icon"
            )

            # Opzionale: un tooltip che spiega lo stato attuale
            ui.label().bind_text_from(manager, "mode", backward=lambda v: f"Stato: {v}")

    with ui.card().classes("w-64 p-4 items-center  mx-auto"):
        ui.label(f"Impostazioni Tema: {manager.mode}").classes("text-bold")

        # Options as a list of strings
        select = ui.select(
            options=options, value=manager.mode, on_change=lambda e: ui.notify(e.value)
        ).classes("w-40")

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

        # # Aggiungiamo 'q-ml-sm' (margin left small) o 'q-mr-md' (margin right medium)
        # select.add_slot('selected-item', '''
        #     <q-icon :props="props" :name="props.opt.label.icon" size="sm" class="q-mr-md"></q-icon>
        # ''')

        # # select.props(':option-label="(opt) => opt.label.label"' , remove='hide-selected')
        # select.props(':option-label="(opt) => opt.label.label"')
        # select.props(':display-value="select.value?.label?.label || select.value"')
        # SLOT 2: Deve essere "LEGGERO" (niente q-item-section!)
        select.add_slot(
            "selected-item",
            """
            <div class="row items-center no-wrap">
                <q-icon :name="props.opt.label.icon" size="sm" class="q-mr-sm"></q-icon>
                <span class="ellipsis">{{ props.opt.label.label }}</span>
            </div>
        """,
        )


if __name__ in {"__main__", "__mp_main__"}:
    ui.run(root, title="theme manager", storage_secret="pippo", port=8081)  # type: ignore
