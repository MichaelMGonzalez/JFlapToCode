# import "macros.jinja.cs" as macros
            // The following switch statement handles the MDP's state transition logic
            switch(state) {
                #- for state in states: 
                case State.{{ state.name }}:
                {{macros.mdp_transition_structure( state.transitions, False)}}
                    break;
            # endfor 
            }
