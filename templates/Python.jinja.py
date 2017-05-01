import time
import threading
import traceback
import sys
class {{ class_name }}AbstractFSM(threading.Thread):
    {%- for state in states %}
    {{ state.name }} = {{state.id}}
    {%- endfor %}
    def __init__(self, delay_rate=.01):
        self.delay_rate = delay_rate
        self.transitioned_at = 0
        self.state = {{ class_name }}AbstractFSM.{{ init_state }}
        self.is_running = True
        self.start_time = time.time()
        threading.Thread.__init__(self)
    def run(self):
        try:
            while self.is_running:
                prevState = self.state;
                # The following switch statement handles the state machine's action logic
                {%- for state in states %}
                {%- if loop.first %}
                if self.state == {{ class_name }}AbstractFSM.{{state.name}}:
                {%- else %}
                elif self.state == {{ class_name }}AbstractFSM.{{state.name}}:
                {%- endif %}
                    self.execute_action_{{ state.name }}()
                {%- endfor %}
                # The following switch statement handles the HLSM's state transition logic
                {%- for state in states %}
                {%- if loop.first %}
                if self.state == {{ class_name }}AbstractFSM.{{ state.name }}:
                {%- else %}
                elif self.state == {{ class_name }}AbstractFSM.{{ state.name }}:
                {%- endif %}
                    {%- for t_name, transition in state.transitions.items() %}
                     {%- if transition.norm and transition.neg %}
                     if self.{{t_name}}(): 
                        self.state = {{ class_name }}AbstractFSM.{{transition.norm}}
                     else: 
                        self.state = {{ class_name }}AbstractFSM.{{transition.neg}}
                     {%- elif transition.norm %}
                     {%- if t_name %}
                     if self.{{t_name}}(): 
                        self.state = {{ class_name }}AbstractFSM.{{transition.norm}}
                     {%- else %}
                     self.state = {{ class_name }}AbstractFSM.{{transition.norm}}
                     {%- endif %}
                     {%- elif transition.neg%}
                     if not self.{{t_name}}():  
                        self.state = {{ class_name }}AbstractFSM.{{transition.neg}}
                     {%- endif %}
                   {%- endfor %}
                     pass
                {%- endfor %}
                time.sleep( self.delay_rate )
                if prevState != self.state:
                    self.transitioned_at = time.time()
                    self.on_transition()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_exception( exc_type, exc_value, exc_traceback )
            input( "Press any key to continue...")
    # State Logic Functions
    {%- for state in states %}
    def execute_action_{{state.name}}(self):
        pass
    {%- endfor %}
    # Transitional Logic Functions
    {%- for transition in transitions %}
    def {{transition}}(self):
        return False
    {%- endfor %}
    def on_transition(self):
        pass
    def get_time_in_state(self):
        return time.time() - self.transitioned_at
    def get_time_since_start(self):
        return time.time() - self.start_time
