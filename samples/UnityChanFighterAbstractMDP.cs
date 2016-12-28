using UnityEngine;
using System;
using System.IO;
using System.Collections;
public abstract class UnityChanFighterAbstractFSM : EnemyGridObject, IStateMachine{
    protected float transitionedAt;
    [Header("State Machine Variables")]
    public int exceptionCount;
    public int shutDownFSMAfterNExceptions = 10;
    public Coroutine coroutine;
    public enum State { 
        Init = 0,
        TurnLeft = 1,
        TurnRight = 2,
        Scan = 3,
        Idle = 4,
        MoveForward = 5,
        WatchingTarget = 6,
        ApproachTarget = 7,
        Punch = 8,
        SideStep = 9,
        CombatScan = 10,
        GainDistance = 11,
        Dashing = 12,
        SlowlyBackup = 13
    }  
    protected virtual void OnEnable() { 
        RunFSM();
    }
    public State state = State.Init;
    private IEnumerator FSMThread( float delayRate ) {
        bool isRunning = true;
        while(isRunning) {
            yield return Tick();
        }
    }
    
    public IEnumerator Tick()
    {
            // Get a uniform random number for MDP transitions
            float rand = UnityEngine.Random.value;
            State prevState = state;
            IEnumerator stateAction = null;
            try {
            // The following switch statement handles the state machine's action logic
                switch(state) {
                    case State.Init:
                        stateAction = ExecuteActionInit();
                        break;
                    case State.TurnLeft:
                        stateAction = ExecuteActionTurnLeft();
                        break;
                    case State.TurnRight:
                        stateAction = ExecuteActionTurnRight();
                        break;
                    case State.Scan:
                        stateAction = ExecuteActionScan();
                        break;
                    case State.Idle:
                        stateAction = ExecuteActionIdle();
                        break;
                    case State.MoveForward:
                        stateAction = ExecuteActionMoveForward();
                        break;
                    case State.WatchingTarget:
                        stateAction = ExecuteActionWatchingTarget();
                        break;
                    case State.ApproachTarget:
                        stateAction = ExecuteActionApproachTarget();
                        break;
                    case State.Punch:
                        stateAction = ExecuteActionPunch();
                        break;
                    case State.SideStep:
                        stateAction = ExecuteActionSideStep();
                        break;
                    case State.CombatScan:
                        stateAction = ExecuteActionCombatScan();
                        break;
                    case State.GainDistance:
                        stateAction = ExecuteActionGainDistance();
                        break;
                    case State.Dashing:
                        stateAction = ExecuteActionDashing();
                        break;
                    case State.SlowlyBackup:
                        stateAction = ExecuteActionSlowlyBackup();
                        break;
                }
            }
            catch( Exception e ) {
                LogException(e);
            }
            yield return stateAction;
            
            
            try {
            
            // The following switch statement handles the MDP's state transition logic
            switch(state) {                case State.Init:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.Scan;
                    }
                    break;
                case State.TurnLeft:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.Scan;
                    }
                    break;
                case State.TurnRight:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.Scan;
                    }
                    break;
                case State.Scan:
                
                    if( true ) {
                        // Probability of transition 10.0%
                        if( rand < 0.1 )
                            state = State.MoveForward;// Probability of transition 10.0%
                        else if( rand < 0.2 )
                        
                            state = State.TurnLeft;// Probability of transition 10.0%
                        else if( rand < 0.30000000000000004 )
                        
                            state = State.TurnRight;// Probability of transition 20.0%
                        else if( rand < 0.5 )
                        
                            state = State.Idle;// Probability of transition 50.0%
                        else
                            state = State.WatchingTarget;
                    }
                    break;
                case State.Idle:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.Scan;
                    }
                    break;
                case State.MoveForward:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.Scan;
                    }
                    break;
                case State.WatchingTarget:
                
                    if( true ) {
                        // Probability of transition 5.555555555555556%
                        if( rand < 0.05555555555555556 )
                            state = State.Dashing;// Probability of transition 5.555555555555556%
                        else if( rand < 0.11111111111111112 )
                        
                            state = State.SideStep;// Probability of transition 16.666666666666664%
                        else if( rand < 0.2777777777777778 )
                        
                            state = State.SlowlyBackup;// Probability of transition 16.666666666666664%
                        else if( rand < 0.4444444444444444 )
                        
                            state = State.WatchingTarget;// Probability of transition 27.77777777777778%
                        else if( rand < 0.7222222222222222 )
                        
                            state = State.ApproachTarget;// Probability of transition 27.77777777777778%
                        else
                            state = State.Punch;
                    }
                    break;
                case State.ApproachTarget:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.CombatScan;
                    }
                    break;
                case State.Punch:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.GainDistance;
                    }
                    break;
                case State.SideStep:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.CombatScan;
                    }
                    break;
                case State.CombatScan:
                
                    if( true ) {
                        // Probability of transition 50.0%
                        if( rand < 0.5 )
                            state = State.GainDistance;// Probability of transition 50.0%
                        else
                            state = State.WatchingTarget;
                    }
                    break;
                case State.GainDistance:
                
                    if( true ) {
                        // Probability of transition 100.0%
                        if( true )
                            state = State.Scan;
                    }
                    break;
                case State.Dashing:
                
                    if( true ) {
                        // Probability of transition 50.0%
                        if( rand < 0.5 )
                            state = State.Dashing;// Probability of transition 50.0%
                        else
                            state = State.Punch;
                    }
                    break;
                case State.SlowlyBackup:
                
                    if( true ) {
                        // Probability of transition 50.0%
                        if( rand < 0.5 )
                            state = State.SlowlyBackup;// Probability of transition 50.0%
                        else
                            state = State.WatchingTarget;
                    }
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
    protected abstract IEnumerator ExecuteActionInit();
    protected abstract IEnumerator ExecuteActionTurnLeft();
    protected abstract IEnumerator ExecuteActionTurnRight();
    protected abstract IEnumerator ExecuteActionScan();
    protected abstract IEnumerator ExecuteActionIdle();
    protected abstract IEnumerator ExecuteActionMoveForward();
    protected abstract IEnumerator ExecuteActionWatchingTarget();
    protected abstract IEnumerator ExecuteActionApproachTarget();
    protected abstract IEnumerator ExecuteActionPunch();
    protected abstract IEnumerator ExecuteActionSideStep();
    protected abstract IEnumerator ExecuteActionCombatScan();
    protected abstract IEnumerator ExecuteActionGainDistance();
    protected abstract IEnumerator ExecuteActionDashing();
    protected abstract IEnumerator ExecuteActionSlowlyBackup();
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