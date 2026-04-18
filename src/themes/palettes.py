from nicegui import ui


def apply_brand_theme():
    """Configura i colori per un look Slate professionale con accenti Blue."""
    ui.colors(
        # Il colore del Brand (il tocco 'giovane')
        primary="#3b82f6",  # Blue-500 (vivace ma serio)
        # I grigi 'Slate' per la struttura (la nostalgia solida)
        secondary="#475569",  # Slate-600 (testi e icone secondarie)
        accent="#0ea5e9",  # Sky-500 (per piccoli dettagli)
        # Dark Mode bilanciato (non nero puro, ma Slate scuro)
        dark="#0f172a",  # Slate-900
        # Stati funzionali
        positive="#10b981",  # Emerald-500
        negative="#ef4444",  # Red-500
        info="#6366f1",  # Indigo-500
        warning="#f59e0b",  # Amber-500
        critical="#8b0000"  # Dark Red-500
    )
