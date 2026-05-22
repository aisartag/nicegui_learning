from typing import Callable

from nicegui import ui, events


class ScreenState:
    def __init__(self, callback: Callable[[bool], None]):

        self.callback = callback

        ui.add_head_html("""
          <script>
                         
                const breakpoint = window.matchMedia("(width < 1024px)");
                            
                const handleBreakpointChange = e => {
                    console.log('is_mobile',e.matches)
                    emitEvent('breakpoint_change', {is_mobile:e.matches});
                    
                } 
                
                   
                window.onload = () => {
                        
                        console.log('is_mobile',breakpoint.matches); 
                        emitEvent('breakpoint_change', {is_mobile:breakpoint.matches} ); 
                        breakpoint.addEventListener('change', handleBreakpointChange);  
                                
                };
               
          </script>
        """)

        ui.on("breakpoint_change", lambda e: self.handle_breakpoint_change(e))

    def handle_breakpoint_change(self, e: events.GenericEventArguments) -> None:
        self.callback(e.args["is_mobile"])
