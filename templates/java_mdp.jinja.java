% import "c_like_macros.jinja" as macros
            // The following switch statement handles the MDP's state transition logic
            switch(state) {
                %- for state in states: 
                case {{ state.name }}:
                {{macros.mdp_transition_structure( state.transitions, False)}}
                    break;
            % endfor 
            }
