#- macro cdf_transitions( transitions )
#- for cdf, transition_state, probability in transitions: 
// Probability of transition {{ probability * 100 }}%
                        {%- if loop.first %}
                        if( rand < {{cdf}} )
                        {%- else %}
                        else if( rand < {{cdf}} )
                        {%- endif %}
                            state = State.{{transition_state}};
#- endfor
#- endmacro
