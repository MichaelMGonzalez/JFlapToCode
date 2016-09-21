%- macro state_name(state)
%- filter upper
%- if state.name
{{ state.name }}_STATE 
%- else
{{state}}_STATE
%- endif
%- endfilter
%- endmacro
% filter upper
#IFNDEF {{class_name}}_HLSM
#DEFINE {{class_name}}_HLSM

% for state in states:
#DEFINE {{state_name(state)}} {{state.id}}
%endfor


% if delays
% for state in delays
#DEFINE DELAY_DURING_{{ state.name }} = {{state.delay}};

% endfor
% endif
% endfilter 

#include <Arduino.h>
#include "{{ class_name }}.h"

class {{ class_name }}_HLSM : {{ class_name }} {
    protected:
        long transitioned_at = 0;
        // State Logic Functions
        % for state in states:
        % if state.has_func and not state.func: 
        void do_{{state.name}}();
        % endif 
        % endfor 
        % for t in user_state_f:
        void do_Execute{{t}}();
        % endfor 
        // Transitional Logic Functions
        % for transition in transitions:
        % if transition: 
        bool {{transition}}();
        % endif 
        % endfor 
        void on_any_transition();
    public:
        short state = {{ state_name(init_state) }};
        void update( ) {
        % if any_state:
        // While in any state, follow these transitions
        % endif
        short prev_state = state;
        // The following switch statement handles the state machine's action logic
            switch(state) {
                % for state in states:
                % if state.has_func:
                    case {{state_name(state)}}:
                        % if state.func: 
                        do_{{ state.func}}();
                        % else:
                        do_{{ state.name }}();
                        % endif 
                        break;
                    % endif 
                    % endfor 
            }
            // The following switch statement handles the HLSM's state transition logic
            switch(state) {
                % for state in states:
                    case {{state_name(state)}}:
                    % for t_name, transition in state.transitions.iteritems(): 
                        % if transition.norm and transition.neg: 
                        if( {{t_name}}() ) 
                            state = {{state_name(transition.norm)}};
                        else 
                            state = {{state_name(transition.norm)}};
                        % elif transition.norm 
                        % if t_name 
                        if( {{t_name}}() ) 
                            state = {{state_name(transition.norm)}};
                        % else 
                        state = {{state_name(transition.norm)}};
                        % endif 
                        % elif transition.neg
                        % if t_name 
                        if( !{{t_name}}() ) 
                            state = {{state_name(transition.norm)}};
                        % else 
                        state = {{state_name(transition.norm)}};
                        % endif 
                        % endif 
                    % endfor 
                        break;
                % endfor 
                }
            if ( prev_state != state ) {
                transitionedAt = millis();
                on_any_transition();
            }
        }

        long time_in_state() {
            return millis() - transitioned_at;
        }
        bool test_and_set(bool & variable, bool val) {
            bool rv = variable;
            variable = val;
            return rv;
        }
}
#ENDIF