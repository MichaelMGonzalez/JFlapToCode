using UnityEngine;
using System;
using System.IO;
using System.Collections;
public abstract class SimpleAIAbstractFSM : MonoBehaviour, IStateMachine{
    protected float transitionedAt;
    public int exceptionCount;
    public int shutDownFSMAfterNExceptions = 10;
    public Coroutine coroutine;
    public float delayDuringSlacking = 5f;
    public enum State { 
        Scan = 0,
        Slacking = 1,
        Attack = 2,
        Tracking = 3,
        RunTowardsPlayer = 4,
        Wander = 5,
        Startled = 6,
        Dazed = 7,
        TakingDamage = 8
    }  
    protected virtual void OnEnable() { 
        RunFSM();
    }
    public State state = State.Scan;
    private IEnumerator FSMThread( float delayRate ) {
        bool isRunning = true;
        while(isRunning) {
            State prevState = state;
            IEnumerator stateAction = null;
            try {
            // The following switch statement handles the state machine's action logic
                switch(state) {
                    case State.Scan:
                        stateAction = ExecuteActionScan();
                        break;
                    case State.Slacking:
                        stateAction = ExecuteActionSlacking();
                        break;
                    case State.Attack:
                        stateAction = ExecuteActionAttack();
                        break;
                    case State.Tracking:
                        stateAction = ExecuteActionTracking();
                        break;
                    case State.RunTowardsPlayer:
                        stateAction = ExecuteActionRunTowardsPlayer();
                        break;
                    case State.Wander:
                        stateAction = ExecuteActionWander();
                        break;
                    case State.Startled:
                        stateAction = ExecuteActionStartled();
                        break;
                    case State.Dazed:
                        stateAction = ExecuteActionDazed();
                        break;
                    case State.TakingDamage:
                        stateAction = ExecuteActionTakingDamage();
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
                case State.Scan:
                    if( SawPlayer() ) 
                        state = State.Tracking;
                    else 
                       state = State.Slacking;
                    break;
                case State.Slacking:
                    if( Wait1Sec() ) 
                        state = State.Wander;
                    break;
                case State.Attack:
                    if( Wait1Sec() ) 
                        state = State.Scan;
                    break;
                case State.Tracking:
                    if( DistanceGT5() ) 
                        state = State.RunTowardsPlayer;
                    else 
                       state = State.Attack;
                    break;
                case State.RunTowardsPlayer:
                    if( Wait1Sec() ) 
                        state = State.Scan;
                    break;
                case State.Wander:
                    if( Wait2Sec() ) 
                        state = State.Scan;
                    if( DistLE3() ) 
                        state = State.Startled;
                    break;
                case State.Startled:
                    if( Wait1Sec() ) 
                        state = State.Tracking;
                    break;
                case State.Dazed:
                    if( Wait1Sec() ) 
                        state = State.Scan;
                    break;
                case State.TakingDamage:
                    if( Wait1Sec() ) 
                        state = State.Dazed;
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
    }

    // State Logic Functions
    protected abstract IEnumerator ExecuteActionScan();
    protected abstract IEnumerator ExecuteActionSlacking();
    protected abstract IEnumerator ExecuteActionAttack();
    protected abstract IEnumerator ExecuteActionTracking();
    protected abstract IEnumerator ExecuteActionRunTowardsPlayer();
    protected abstract IEnumerator ExecuteActionWander();
    protected abstract IEnumerator ExecuteActionStartled();
    protected abstract IEnumerator ExecuteActionDazed();
    protected abstract IEnumerator ExecuteActionTakingDamage();
    // Transitional Logic Functions
    protected abstract bool SawPlayer();
    protected abstract bool Wait2Sec();
    protected abstract bool DistLE3();
    protected abstract bool DistanceGT5();
    protected abstract bool Wait1Sec();
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
        exceptionAcc += " while in " + state + "\n";
        if( exceptionCount++ == 0 ) {
            DateTime now = DateTime.Now;
            string errorLogFileName = (Application.dataPath + "/Exceptions/");
            errorLogFileName += now.Year + "_" + now.Month + "_" + now.Day + "/" + GetType() + "/";
            errorLogFileName = errorLogFileName.Replace("/","\\");
            try {
                Directory.CreateDirectory(errorLogFileName);
                errorLogFileName += DateTime.Now.ToFileTime() + "_" + "(" + e.GetType() + ").txt";
                File.WriteAllText( errorLogFileName, exceptionAcc + e.StackTrace );
                exceptionAcc += "Full details logged to: " + errorLogFileName + "\n";
                exceptionAcc += e.StackTrace;
            }
            catch(Exception e2) { Debug.LogError("Could not create exceptions directory" + e2.GetType()); }
        }
        Debug.LogError( exceptionAcc );
    }
    protected virtual void OnTransition() { }
    public abstract void Reset();
}