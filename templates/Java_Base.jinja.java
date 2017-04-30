%- import "c_like_macros.jinja" as macros
{%- block macro_block %}
{%- endblock %}
{%- block libraries %}
import java.util.Random;
{% endblock %}
{%- set return_type = 'void' %}
public abstract class {{ class_name }}{% block inheritance %}AbstractFSM{% endblock %} {
	{%- block variables %} 
    private static Random rng = new Random();
    public enum State { 
    % for state in states:
        {{ state.name }}{% if not loop.last %},{%endif%}
        %endfor 
    }  
    public State state = State.{{ init_state }};
	{%- endblock %}
    
	{%- block extra_functions %}
    protected abstract void OnTransition();
	{%- endblock %}
    public {{return_type}} Step()
    {
		State prevState = state;
		% if type == "mealy":
            // Get a uniform random number for MDP transitions
            float rand = rng.nextFloat();
		% endif
        %- if any_state:
            // While in any state, follow these transitions
			%- if type == "mealy":
            {{macros.mdp_transition_structure( any_state.transitions, True)}}
			% endif
        %- endif
		{% block state_action %} 
                switch(state) {
                % for state in states:
                % if state.has_func:
                    case {{state.name}}:
                    % if state.func: 
                        Execute{{ state.func}}();
                    % else:
                        ExecuteAction{{ state.name }}();
                    % endif 
                        break;
                % endif 
                % endfor 
            }
		{%- endblock %}
        {%- block transition %}
        % if type == "mealy" 
        % include "java_mdp.jinja.java" 
        % else 
        % include "java_hlsm.jinja.java" 
        % endif 
		{% endblock %}
		{% block end_of_tick %}
            if (prevState != state)
            {
                OnTransition();
            }
			{% endblock %}
    }
    // State Logic Functions
    % for state in states:
    % if state.has_func and not state.func: 
    protected abstract {{return_type}} ExecuteAction{{state.name}}();
    % endif 
    % endfor 
    % for t in user_state_f:
    protected abstract {{return_type}} Execute{{t}}();
    % endfor 
    // Transitional Logic Functions
    % for transition in transitions:
    % if transition: 
    protected abstract boolean {{transition}};
    % endif 
    % endfor 
    


    
    
  
}