% import "macros.jinja.cs" as macros
using UnityEngine;
using System;
using System.IO;
using System.Collections;
public abstract class {{ class_name }}AbstractFSM : EnemyGridObject, IStateMachine{
    protected float transitionedAt;
    [Header("State Machine Variables")]
    public int exceptionCount;
    public int shutDownFSMAfterNExceptions = 10;
    public Coroutine coroutine;
    % if delays
    % for state in delays
    public float delayDuring{{ state.name }} = {{state.delay}};
    % endfor
    % endif
    public enum State { 
        % for state in states:
        {{ state.name }} = {{state.id}}{% if not loop.last %},{%endif%}
        %endfor 
    }  
    protected virtual void OnEnable() { 
        RunFSM();
    }
    public State state = State.{{ init_state }};
    private IEnumerator FSMThread( float delayRate ) {
        bool isRunning = true;
        while(isRunning) {
            yield return Tick();
        }
    }
    
    public IEnumerator Tick()
    {
    % if type == "mealy":
            // Get a uniform random number for MDP transitions
            float rand = UnityEngine.Random.value;
            % endif
            %- if any_state:
            // While in any state, follow these transitions
            %- if type == "mealy":
            {{macros.mdp_transition_structure( any_state.transitions, True)}}
            % endif
            %- endif
            State prevState = state;
            IEnumerator stateAction = null;
            try {
            // The following switch statement handles the state machine's action logic
                switch(state) {
                % for state in states:
                % if state.has_func:
                    case State.{{state.name}}:
                    % if state.func: 
                        stateAction = Execute{{ state.func}}();
                    % else:
                        stateAction = ExecuteAction{{ state.name }}();
                    % endif 
                        break;
                % endif 
                % endfor 
                }
            }
            catch( Exception e ) {
                LogException(e);
            }
            yield return stateAction;
            
            
            try {
            
            % if type == "mealy" 
            % include "Unity_MDP.jinja.cs" 
            % else 
            % include "Unity_HLSM.jinja.cs" 
            % endif 
            
            }
            catch(Exception e) {
                LogException(e);
            }
            yield return new WaitForSeconds( delayRate );
            if( exceptionCount > shutDownFSMAfterNExceptions )
            {
                Debug.LogError( this + " has exceeded the number of allowed exceptions! Shutting down.");
                isRunning = false;
            }
            else if ( prevState!=state ) {
                transitionedAt = Time.time;
                OnTransition();
            }
    }

    // State Logic Functions
    % for state in states:
    % if state.has_func and not state.func: 
    protected abstract IEnumerator ExecuteAction{{state.name}}();
    % endif 
    % endfor 
    % for t in user_state_f:
    protected abstract IEnumerator Execute{{t}}();
    % endfor 
    // Transitional Logic Functions
    % for transition in transitions:
    % if transition: 
    protected abstract bool {{transition}}();
    % endif 
    % endfor 
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
    protected void LogException(Exception e) {
        string exceptionAcc = this + " threw exception " + e.GetType();
        exceptionAcc += " during state: " + state + "\n";
        #if (EXCEPTION_LOGGER)
		if( exceptionCount++ == 0 ) {
			var dest = ExceptionLogger.LogException(e, exceptionAcc, this);
			exceptionAcc += "Full details logged to: " + dest + "\n";
			exceptionAcc += e.StackTrace;
		}
		#else
		exceptionCount++;
		#endif
        Debug.LogError( exceptionAcc );
    }
    protected virtual void OnTransition() { }
    public abstract void Reset();
}