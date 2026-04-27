from nicegui import ui


def button_nav(label: str, path: str, icon: str, is_on_header: bool = False):
    
    btn = (
        ui.button(label, icon=icon, on_click=lambda: ui.navigate.to(path)).props("flat no-caps")
    )
   
    btn.props("color=white") if is_on_header else btn.props("color=primary")
    return btn

