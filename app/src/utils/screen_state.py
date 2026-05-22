from typing import Callable

from nicegui import ui


class ScreenState:
    def __init__(self, callback: Callable[[bool], None]):

        self.callback = callback

        ui.add_head_html("""
          <script>
                         
                const breakpoint = window.matchMedia("(width < 1024px)");
                            
                const handleBreakpointChange = e => {
                    console.log('is_mobile',e.matches)
                    emitEvent('bp_sync', {is_mobile:e.matches});
                    
                } 
                
                   
                window.onload = () => {
                        
                        console.log('is_mobile',breakpoint.matches); 
                        emitEvent('bp_sync', {is_mobile:breakpoint.matches} ); 
                        breakpoint.addEventListener('change', handleBreakpointChange);  
                                
                };
               
          </script>
        """)

        # ui.on("bp_sync", lambda e: self.handle_breakpoint_change(e))

        ui.on("bp_sync", lambda e: self.callback(e.args["is_mobile"]))

    # def handle_breakpoint_change(self, e:events.GenericEventArguments) -> None:
    #     self.callback(e.args['is_mobile'])
