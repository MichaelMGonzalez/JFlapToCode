{%- if any_state %}
// While in any state, follow these transitions deterministically
    {%- for t_name, transition in any_state.transitions.iteritems() %}
           {%- if transition.norm and transition.neg %}
            if( {{t_name}}() ) 
                state = State.{{transition.norm}};
            else 
               state = State.{{transition.neg}};
            {%- elif transition.norm %}
                    {%- if t_name %}
            if( {{t_name}}() ) 
                state = State.{{transition.norm}};
            {%- else %}
            state = State.{{transition.norm}};
            {%- endif %}
            {%- elif transition.neg%}
            {%- if t_name %}
            if( !{{t_name}}() ) 
                state = State.{{transition.neg}};
            {%- else %}
            state = State.{{transition.neg}};
            {%- endif %}
            {%- endif %}
        {%- endfor %}
    {%- endif %}
// The following switch statement handles the HLSM's state transition logic
            switch(state) {
                {%- for state in states %}
                case {{ state.name }}:
                {%- for t_name, transition in state.transitions.items() %}
                    {%- if transition.norm and transition.neg %}
                    if( {{t_name}} ) 
                        state = State.{{transition.norm}};
                    else 
                       state = State.{{transition.neg}};
                    {%- elif transition.norm %}
                    {%- if t_name %}
                    if( {{t_name}} ) 
                        state = State.{{transition.norm}};
                    {%- else %}
                    state = State.{{transition.norm}};
                    {%- endif %}
                    {%- elif transition.neg%}
                    {%- if t_name %}
                    if( !{{t_name}} ) 
                        state = State.{{transition.neg}};
                    {%- else %}
                    state = State.{{transition.neg}};
                    {%- endif %}
                    {%- endif %}
               {%- endfor %}
                    break;
            {%- endfor %}
            }
