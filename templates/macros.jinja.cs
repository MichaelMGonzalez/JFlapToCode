#- macro cdf_transitions( transitions )
#- for cdf, transition_state, probability in transitions: 
// Probability of transition {{ probability * 100 }}%
                        {%- if loop.length == 1 %}
                        if( true )
                        {%- elif loop.first %}
                        if( rand < {{cdf}} )
                        {%- elif loop.last %}
                        else
                        {%- else %}
                        else if( rand < {{cdf}} )
                        {% endif %}
                            state = State.{{transition_state}};
#- endfor
#- endmacro

#- macro mdp_transition_structure( transition_set, continue )
            #- for t_name, transition in transition_set.iteritems(): 
            #- if transition.norm and transition.neg
                    {%- if t_name %}
                    if( {{t_name}}() ) {
                    {%- else %}
                    if( true ) {
                    {%- endif %}
                        {{cdf_transitions( transition.norm)}}
                        {{should_continue( continue )}}
                    }
                    else {
                        {{cdf_transitions( transition.neg)}}
                        {{should_continue( continue )}}
                    }
                    {%- elif transition.norm %}
                    {%- if t_name %}
                    if( {{t_name}}() ) {
                    {%- else %}
                    if( true ) {
                    {%- endif %}
                        {{cdf_transitions( transition.norm)}}
                        {{should_continue( continue )}}
                    }
                    {%- elif transition.neg%}
                    if( !{{t_name}}() ) {
                        {{cdf_transitions( transition.neg )}}
                        {{should_continue( continue )}}
                    }
            #- endif 
        #- endfor 
#- endmacro

#- macro should_continue( val )
#- if val 
continue;
#- endif
#- endmacro

