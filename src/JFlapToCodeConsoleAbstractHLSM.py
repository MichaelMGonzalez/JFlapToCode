import time
import threading
import traceback
import sys
class JFlapToCodeConsoleAbstractFSM(threading.Thread):
    prompt_auto = 0
    automate = 1
    display_config = 2
    init = 3
    console_animation = 4
    exit = 6
    def __init__(self, delay_rate=.01):
        self.delay_rate = delay_rate
        self.transitioned_at = 0
        self.state = JFlapToCodeConsoleAbstractFSM.init
        self.is_running = True
        self.start_time = time.time()
        threading.Thread.__init__(self)
    def run(self):
        try:
            while self.is_running:
                prevState = self.state;
                # The following switch statement handles the state machine's action logic
                if self.state == JFlapToCodeConsoleAbstractFSM.prompt_auto:
                    self.execute_action_prompt_auto()
                elif self.state == JFlapToCodeConsoleAbstractFSM.automate:
                    self.execute_action_automate()
                elif self.state == JFlapToCodeConsoleAbstractFSM.display_config:
                    self.execute_action_display_config()
                elif self.state == JFlapToCodeConsoleAbstractFSM.init:
                    self.execute_action_init()
                elif self.state == JFlapToCodeConsoleAbstractFSM.console_animation:
                    self.execute_action_console_animation()
                elif self.state == JFlapToCodeConsoleAbstractFSM.exit:
                    self.execute_action_exit()
                # The following switch statement handles the HLSM's state transition logic
                if self.state == JFlapToCodeConsoleAbstractFSM.prompt_auto:
                     if self.should_auto_continue(): 
                        self.state = JFlapToCodeConsoleAbstractFSM.automate
                     if self.should_refresh_anim(): 
                        self.state = JFlapToCodeConsoleAbstractFSM.console_animation
                     if self.enter_config(): 
                        self.state = JFlapToCodeConsoleAbstractFSM.display_config
                     pass
                elif self.state == JFlapToCodeConsoleAbstractFSM.automate:
                     self.state = JFlapToCodeConsoleAbstractFSM.exit
                     pass
                elif self.state == JFlapToCodeConsoleAbstractFSM.display_config:
                     if self.should_parse(): 
                        self.state = JFlapToCodeConsoleAbstractFSM.automate
                     pass
                elif self.state == JFlapToCodeConsoleAbstractFSM.init:
                     if self.has_file_to_parse(): 
                        self.state = JFlapToCodeConsoleAbstractFSM.prompt_auto
                     else: 
                        self.state = JFlapToCodeConsoleAbstractFSM.display_config
                     pass
                elif self.state == JFlapToCodeConsoleAbstractFSM.console_animation:
                     self.state = JFlapToCodeConsoleAbstractFSM.prompt_auto
                     pass
                elif self.state == JFlapToCodeConsoleAbstractFSM.exit:
                     pass
                time.sleep( self.delay_rate )
                if prevState != self.state:
                    self.transitioned_at = time.time()
                    self.on_transition()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception( exc_type, exc_value, exc_traceback )
            input( "Press any key to continue...")
    # State Logic Functions
    def execute_action_prompt_auto(self):
        pass
    def execute_action_automate(self):
        pass
    def execute_action_display_config(self):
        pass
    def execute_action_init(self):
        pass
    def execute_action_console_animation(self):
        pass
    def execute_action_exit(self):
        pass
    # Transitional Logic Functions
    def has_file_to_parse(self):
        return False
    def should_auto_continue(self):
        return False
    def should_refresh_anim(self):
        return False
    def should_parse(self):
        return False
    def enter_config(self):
        return False
    def on_transition(self):
        pass
    def get_time_in_state(self):
        return time.time() - self.transitioned_at
    def get_time_since_start(self):
        return time.time() - self.start_time