using UnityEngine;
using System.Collections;
public abstract class SimpleAIAbstractFSM : MonoBehaviour, IStateMachine{
    protected float transitionedAt;
    public float delayWhileSlacking = 5f;
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
    public State state = State.Scan;
    private IEnumerator FSMThread( float delayRate ) {
        while(true) {
            State prevState = state;
            // The following switch statement handles the state machine's action logic
            switch(state) {
                case State.Scan:
                    yield return ExecuteActionScan();
                    break;
                case State.Slacking:
                    yield return ExecuteActionSlacking();
                    break;
                case State.Attack:
                    yield return ExecuteActionAttack();
                    break;
                case State.Tracking:
                    yield return ExecuteActionTracking();
                    break;
                case State.RunTowardsPlayer:
                    yield return ExecuteActionRunTowardsPlayer();
                    break;
                case State.Wander:
                    yield return ExecuteActionWander();
                    break;
                case State.Startled:
                    yield return ExecuteActionStartled();
                    break;
                case State.Dazed:
                    yield return ExecuteActionDazed();
                    break;
                case State.TakingDamage:
                    yield return ExecuteActionTakingDamage();
                    break;
            }
            
            

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
            }            yield return new WaitForSeconds( delayRate );

            if ( prevState!=state ) {
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
        StartCoroutine(FSMThread(delayRate));
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