# route_events.py
from nicegui import Event

# L'evento può opzionalmente passare dati (str, dict, ecc.)
childrens_emitted = Event[list[dict[str, str]] | None]()
