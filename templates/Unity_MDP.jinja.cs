# import "macros.jinja.cs" as macros
// Get a uniform random number for MDP transitions
            float rand = Random.value;
 #//This is a test comment
{%- if any_state %}
            // While in any state, follow these transitions
{%- for t_name, transition in any_state.transitions.iteritems() %}
                    {%- if transition.norm and transition.neg %}
                    {%- if t_name %}
                    if( {{t_name}}() ) {
                    {%- else %}
                    if( true ) {
                    {%- endif %}
                        {{macros.cdf_transitions( transition.norm)}}
                        continue;
                    }
                    else {
                        {{macros.cdf_transitions( transition.neg)}}
                        continue;
                    }
                    {%- elif transition.norm %}
                    {%- if t_name %}
                    if( {{t_name}}() ) {
                    {%- else %}
                    if( true ) {
                    {%- endif %}
                        {{macros.cdf_transitions( transition.norm)}}
                        continue;
                    }
                    {%- elif transition.neg%}
                    if( !{{t_name}}() ) {
                        {{macros.cdf_transitions( transition.neg )}}
                        continue;
                    }
                    {%- endif %}
               {%- endfor %}
{%- endif %}


            // The following switch statement handles the MDP's state transition logic
            switch(state) {
                {%- for state in states %}
                case State.{{ state.name }}:
                {%- for t_name, transition in state.transitions.iteritems() %}
                    #// This section deals with normal transitions and negated transitions
                    {%- if transition.norm and transition.neg %}
                    {%- if t_name %}
                    if( {{t_name}}() ) {
                    {%- else %}
                    if( true ) {
                    {%- endif %}
                        {{macros.cdf_transitions( transition.norm )}}
                    }
                    else {
                        {{macros.cdf_transitions( transition.neg )}}
                    }
                    #// This section deals with normal transitions
                    {%- elif transition.norm %}
                    {%- if t_name %}
                    if( {{t_name}}() ) {
                    {%- else %}
                    if( true ) {
                    {%- endif %}
                        {{macros.cdf_transitions( transition.norm )}}
                    }
                    #// This section deals with negated transitions
                    {%- elif transition.neg%}
                    if( !{{t_name}}() ) {
                        {{macros.cdf_transitions( transition.neg )}}
                    }
                    {%- endif %}
               {%- endfor %}
                    break;
            {%- endfor %}
            }
