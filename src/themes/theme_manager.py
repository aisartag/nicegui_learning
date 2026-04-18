from typing import Literal, cast, Any, Dict, get_args
from nicegui import ui


# Definiamo i valori ammessi per il tema (Literal è perfetto per Pyright Strict)
ThemeLiteral = Literal["light", "dark", "auto"]


class ThemeManager:
    # Mappa delle icone (Material Icons di default in NiceGUI)
    ICONS: Dict[ThemeLiteral, str] = {
        "light": "light_mode",
        "dark": "dark_mode",
        "auto": "settings_brightness",
    }

    # 1. Tipizziamo lo storage come PersistentDict
    def __init__(self, storage: Dict[str, Any]) -> None:
        self.storage = storage
        # setdefault restituisce Any, quindi facciamo un check o un cast se necessario
        if "theme_mode" not in self.storage or self.storage["theme_mode"] is None:
            self.storage["theme_mode"] = "auto"
        self.apply()

    @property
    def mode(self) -> ThemeLiteral:
        # 2. Usiamo cast per assicurare a Pyright che il valore sia uno dei 3 ammessi
        return cast(ThemeLiteral, self.storage.get("theme_mode", "auto"))

    @mode.setter
    def mode(self, value: ThemeLiteral) -> None:
        self.storage["theme_mode"] = value
        self.apply()

    @property
    def icon(self) -> str:
        # Restituisce l'icona corretta in base al modo attuale
        return self.ICONS[self.mode]

    def apply(self) -> None:
        # 3. Ora Pyright sa esattamente cosa contiene self.mode
        if self.mode == "light":
            ui.dark_mode().disable()
        elif self.mode == "dark":
            ui.dark_mode().enable()
        else:
            # .set_value(None) è il modo standard di NiceGUI per 'auto'
            ui.dark_mode().set_value(None)

    def cycle(self) -> None:
        # Ruota tra i 3 stati
        options = list(get_args(ThemeLiteral))
        current_idx = options.index(self.mode)
        next_mode = cast(ThemeLiteral, options[(current_idx + 1) % len(options)])
        self.mode = next_mode





