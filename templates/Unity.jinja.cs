{% extends "c_like_base.jinja" %}
{%  block inheritance %}FSM: {%- if namespace %} {{namespace}}.{%-endif%}{{super_class}}, IStateMachine{% endblock %}
{% block libraries %}
using UnityEngine;
using System;
using System.IO;
using System.Collections;
{% endblock %}
{% set return_type = 'IEnumerator' %}

{% block variables %}
    {{super()}}
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
    public State state = State.{{ init_state }};{% endblock %}
{% block extra_functions %}
    protected virtual void OnEnable() { 
        RunFSM();
    }
    private IEnumerator FSMThread( float delayRate ) {
        bool isRunning = true;
        while(isRunning) {
            yield return Step();
            yield return new WaitForSeconds(delayRate);
            if (exceptionCount > shutDownFSMAfterNExceptions)
            {
                Debug.LogError(this + " has exceeded the number of allowed exceptions! Shutting down.");
                isRunning = false;
            }
        }
    }
	public void RunFSM()
    {
        RunFSM(Time.fixedDeltaTime);
    }
    public void RunFSM(float delayRate)
    {
        coroutine = StartCoroutine(FSMThread(delayRate));
    }
    public float TimeInState() {
        return Time.time - transitionedAt;
    }
    
    public virtual void OnTransition() {}

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
	public abstract void Reset();
{% endblock %}

{% block transition %}
            try {
                {{super()}}
            }
            catch(Exception e) {
                LogException(e);
            }
            
{% endblock %}

{% block state_action %}
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
{% endblock %}