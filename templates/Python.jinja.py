import time
class {{ class_name }}AbstractFSM:
    {%- for state in states %}
    {{ state.name }} = {{state.id}}
    {%- endfor %}
    def __init__(self, delay_rate=.01):
        self.delay_rate = delay_rate
        self.transitioned_at = 0
        self.state = {{ class_name }}AbstractFSM.{{ init_state }}
    def run(self):
        while True:
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
                {%- for t_name, transition in state.transitions.iteritems() %}
                 {%- if transition.norm and transition.neg %}
                 if self.{{t_name}}(): 
                    self.state = {{ class_name }}AbstractFSM.{{transition.norm}}
                 else: 
                    self.state = {{ class_name }}AbstractFSM.{{transition.neg}}
                 {%- elif transition.norm %}
                 if self.{{t_name}}(): 
                    self.state = {{ class_name }}AbstractFSM.{{transition.norm}}
                 {%- elif transition.neg%}
                 if not self.{{t_name}}():  
                    self.state = {{ class_name }}AbstractFSM.{{transition.neg}}
                 {%- endif %}
               {%- endfor %}
            {%- endfor %}
            time.sleep( self.delay_rate )
            if prevState != self.state:
                self.transitioned_at = time.time
                self.on_transition()
    # State Logic Functions
    {%- for state in states %}
    def execute_action_{{state.name}}(self):
        pass
    {%- endfor %}
    # Transitional Logic Functions
    {%- for transition in transitions %}
    def {{transition}}(self):
        pass
    {%- endfor %}
    def on_transition(self):
        pass
