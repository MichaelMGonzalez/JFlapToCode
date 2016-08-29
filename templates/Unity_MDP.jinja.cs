# import "macros.jinja.cs" as macros
// Get a uniform random number for MDP transitions
            float rand = Random.value;
# if any_state 
            // While in any state, follow these transitions
{{macros.mdp_transition_structure( any_state.transitions, True)}}
#- endif 
            // The following switch statement handles the MDP's state transition logic
            switch(state) {
                #- for state in states: 
                case State.{{ state.name }}:
                {{macros.mdp_transition_structure( state.transitions, False)}}
                    break;
            # endfor 
            }
