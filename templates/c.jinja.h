%- macro state_name(state)
%- filter upper
%- if state.name
{{ state.name }}_STATE 
%- else
{{state}}_STATE
%- endif
%- endfilter
%- endmacro
#ifdef __cplusplus
extern "C" {
#endif
#ifndef {{state_name(class_name)}}_STATE_MACHINE
#define {{state_name(class_name)}}_STATE_MACHINE

% for state in states:
#define {{state_name(state)}} {{state.id}}
%endfor


% if delays
% for state in delays
#define DELAY_DURING_{{ state_name(state) }} = {{state.delay}};
% endfor
% endif

% block libs
% endblock
long transitioned_at = 0;
short state = {{ state_name(init_state) }};
// State Logic Functions
% for state in states :
% if state.has_func and not state.func :
extern void do_{{ state.name }}(void);
% endif
% endfor
% for t in user_state_f :
extern void do_Execute{{ t }}(void);
% endfor
// Transitional Logic Functions
% for transition in transitions :
% if transition :
extern boolean {{ transition }}(void);
% endif
% endfor
extern void on_any_transition(void);
void update_states(void) {
	% if any_state:
	// While in any state, follow these transitions
	% endif
	short prev_state = state;
	// The following switch statement handles the state machine's action logic
	switch (state) {
		% for state in states :
		% if state.has_func :
	case {{state_name(state)}}:
		% if state.func :
			do_{{ state.func }}();
		% else :
			do_{{ state.name }}();
		% endif
			break;
		% endif
			% endfor
	}
	// The following switch statement handles the HLSM's state transition logic
	switch (state) {
		% for state in states :
	case {{state_name(state)}}:
		% for t_name, transition in state.transitions.items() :
			% if transition.norm and transition.neg :
			if ({{ t_name }})
				state = {{ state_name(transition.norm) }};
			else
				state = {{ state_name(transition.norm) }};
		% elif transition.norm
			% if t_name
			if ({{ t_name }})
				state = {{ state_name(transition.norm) }};
		% else
			state = {{ state_name(transition.norm) }};
		% endif
			% elif transition.neg
			% if t_name
			if (!{{t_name}})
				state = {{ state_name(transition.neg) }};
		% else
			state = {{ state_name(transition.norm) }};
		% endif
			% endif
			% endfor
			break;
		% endfor
	}
	if (prev_state != state) {
		transitioned_at = millis();
		on_any_transition();
	}
}

long time_in_state() {
	return millis() - transitioned_at;
}
boolean test_and_set(boolean * variable, boolean val) {
	boolean rv = *variable;
	*variable = val;
	return rv;
}
#endif
#ifdef __cplusplus
}
#endif
