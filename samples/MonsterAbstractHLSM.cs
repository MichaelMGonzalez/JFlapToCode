using UnityEngine;
using System;
using System.IO;
using System.Collections;
public abstract class MonsterAbstractFSM : EnemyGridObject, IStateMachine{
    protected float transitionedAt;
    [Header("State Machine Variables")]
    public int exceptionCount;
    public int shutDownFSMAfterNExceptions = 10;
    public Coroutine coroutine;
    public enum State { 
        Idle = 0,
        Nibble = 1,
        Scan = 2
    }  
    protected virtual void OnEnable() { 
        RunFSM();
    }
    public State state = State.Idle;
    private IEnumerator FSMThread( float delayRate ) {
        bool isRunning = true;
        while(isRunning) {
            yield return Tick();
        }
    }
    
    public IEnumerator Tick()
    {
            State prevState = state;
            IEnumerator stateAction = null;
            try {
            // The following switch statement handles the state machine's action logic
                switch(state) {
                    case State.Idle:
                        stateAction = ExecuteActionIdle();
                        break;
                    case State.Nibble:
                        stateAction = ExecuteActionNibble();
                        break;
                    case State.Scan:
                        stateAction = ExecuteActionScan();
                        break;
                }
            }
            catch( Exception e ) {
                LogException(e);
            }
            yield return stateAction;
            
            
            try {
            

// The following switch statement handles the HLSM's state transition logic
            switch(state) {
                case State.Idle:
                    state = State.Nibble;
                    break;
                case State.Nibble:
                    state = State.Scan;
                    break;
                case State.Scan:
                    state = State.Idle;
                    break;
            }            }
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
    protected abstract IEnumerator ExecuteActionIdle();
    protected abstract IEnumerator ExecuteActionNibble();
    protected abstract IEnumerator ExecuteActionScan();
    // Transitional Logic Functions
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