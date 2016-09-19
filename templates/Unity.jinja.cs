# import "macros.jinja.cs" as macros
using UnityEngine;
using System.Collections;
public abstract class {{ class_name }}AbstractFSM : MonoBehaviour, IStateMachine{
    protected float transitionedAt;
    # if delays
    # for state in delays
    public float delayDuring{{ state.name }} = {{state.delay}};
    # endfor
    # endif
    public enum State { 
        # for state in states:
        {{ state.name }} = {{state.id}}{% if not loop.last %},{%endif%}
        #endfor 
    }  
    public Coroutine coroutine;
    public State state = State.{{ init_state }};

    protected void OnEnable() { 
        RunFSM();
    }
    private IEnumerator FSMThread( float delayRate ) {
        while(true) {
            # if type == "mealy":
            // Get a uniform random number for MDP transitions
            float rand = Random.value;
            # endif
            #- if any_state:
            // While in any state, follow these transitions
            #- if type == "mealy":
            {{macros.mdp_transition_structure( any_state.transitions, True)}}
            # endif
            #- endif
            State prevState = state;
            // The following switch statement handles the state machine's action logic
            switch(state) {
                # for state in states:
                # if state.has_func:
                case State.{{state.name}}:
                    # if state.func: 
                    yield return Execute{{ state.func}}();
                    # else:
                    yield return ExecuteAction{{ state.name }}();
                    # endif 
                    break;
                # endif 
                # endfor 
            }
            
            
            # if type == "mealy" 
            # include "Unity_MDP.jinja.cs" 
            # else 
            # include "Unity_HLSM.jinja.cs" 
            # endif 

            yield return new WaitForSeconds( delayRate );

            if ( prevState!=state ) {
                transitionedAt = Time.time;
                OnTransition();
            }
        }
    }

    // State Logic Functions
    # for state in states:
    # if state.has_func and not state.func: 
    protected abstract IEnumerator ExecuteAction{{state.name}}();
    # endif 
    # endfor 
    # for t in user_state_f:
    protected abstract IEnumerator Execute{{t}}();
    # endfor 
    // Transitional Logic Functions
    # for transition in transitions:
    # if transition: 
    protected abstract bool {{transition}}();
    # endif 
    # endfor 
    public void RunFSM()
    {
        RunFSM(Time.fixedDeltaTime);
    }
    public void RunFSM(float delayRate)
    {
        coroutine = StartCoroutine(FSMThread(delayRate));
    }
    public float TimeInState()
    {
        return Time.time - transitionedAt;
    }
    public bool TestAndSet(ref bool variable, bool val) {
        bool rv = variable;
        variable = val;
        return rv;
    }
    protected virtual void OnTransition() { }
    public abstract void Reset();
}
