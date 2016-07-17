using UnityEngine;
using System.Collections;
public abstract class UnityChanFighterAbstractFSM : AbstractFSM {
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
    public State state = State.Init;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) {
            State prevState = state;
            // The following switch statement handles the state machine's action logic
            switch(state) {
                case State.Init:
                    yield return ExecuteActionInit();
                    break;
                case State.TurnLeft:
                    yield return ExecuteActionTurnLeft();
                    break;
                case State.TurnRight:
                    yield return ExecuteActionTurnRight();
                    break;
                case State.Scan:
                    yield return ExecuteActionScan();
                    break;
                case State.Idle:
                    yield return ExecuteActionIdle();
                    break;
                case State.MoveForward:
                    yield return ExecuteActionMoveForward();
                    break;
                case State.WatchingTarget:
                    yield return ExecuteActionWatchingTarget();
                    break;
                case State.ApproachTarget:
                    yield return ExecuteActionApproachTarget();
                    break;
                case State.Punch:
                    yield return ExecuteActionPunch();
                    break;
                case State.SideStep:
                    yield return ExecuteActionSideStep();
                    break;
                case State.CombatScan:
                    yield return ExecuteActionCombatScan();
                    break;
                case State.GainDistance:
                    yield return ExecuteActionGainDistance();
                    break;
                case State.Dashing:
                    yield return ExecuteActionDashing();
                    break;
                case State.SlowlyBackup:
                    yield return ExecuteActionSlowlyBackup();
                    break;
            }
            
            // Get a uniform random number for MDP transitions
            float rand = Random.value;

            // The following switch statement handles the MDP's state transition logic
            switch(state) {
                case State.Init:
                    if( InitialWait() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Scan;
                    }
                    break;
                case State.TurnLeft:
                    if( ScanWait() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Scan;
                    }
                    break;
                case State.TurnRight:
                    if( ScanWait() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Scan;
                    }
                    break;
                case State.Scan:
                    if( SensesTarget() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.WatchingTarget;
                    }
                    else { 
                        // Probability of transition 20.0%
                        if( rand < 0.2 )
                            state = State.MoveForward; 
                        // Probability of transition 20.0%
                        else if( rand < 0.4 )
                            state = State.TurnLeft; 
                        // Probability of transition 20.0%
                        else if( rand < 0.6 )
                            state = State.TurnRight; 
                        // Probability of transition 40.0%
                        else if( rand < 1.0 )
                            state = State.Idle;
                    }
                    break;
                case State.Idle:
                    if( ScanWait() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Scan;
                    }
                    break;
                case State.MoveForward:
                    if( ScanWait() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Scan;
                    }
                    break;
                case State.WatchingTarget:
                    if( TargetInRange() ) { 
                        // Probability of transition 12.5%
                        if( rand < 0.125 )
                            state = State.Dashing; 
                        // Probability of transition 12.5%
                        else if( rand < 0.25 )
                            state = State.SideStep; 
                        // Probability of transition 37.5%
                        else if( rand < 0.625 )
                            state = State.SlowlyBackup; 
                        // Probability of transition 37.5%
                        else if( rand < 1.0 )
                            state = State.WatchingTarget;
                    }
                    else { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.ApproachTarget;
                    }
                    if( InPunchingRange() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Punch;
                    }
                    break;
                case State.ApproachTarget:
                    if( WaitApproach() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.CombatScan;
                    }
                    break;
                case State.Punch:
                    if( WaitPunch() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.GainDistance;
                    }
                    break;
                case State.SideStep:
                    if( WaitDodge() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.CombatScan;
                    }
                    break;
                case State.CombatScan:
                    if( SensesTarget() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.WatchingTarget;
                    }
                    else { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.GainDistance;
                    }
                    break;
                case State.GainDistance:
                    if( WaitJumpBack() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Scan;
                    }
                    break;
                case State.Dashing:
                    if( InPunchingRange() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Punch;
                    }
                    else { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.Dashing;
                    }
                    break;
                case State.SlowlyBackup:
                    if( TargetInRange() ) { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.SlowlyBackup;
                    }
                    else { 
                        // Probability of transition 100.0%
                        if( rand < 1.0 )
                            state = State.WatchingTarget;
                    }
                    break;
            }
            
            
            yield return new WaitForSeconds( delayRate );
            if ( prevState!=state ) {
                transitionedAt = Time.time;
                OnTransition();
            }
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
    protected abstract bool TargetInRange();
    
    protected abstract bool WaitApproach();
    
    protected abstract bool SensesTarget();
    
    protected abstract bool InPunchingRange();
    
    protected abstract bool ScanWait();
    
    protected abstract bool WaitPunch();
    
    protected abstract bool InitialWait();
    
    protected abstract bool WaitDodge();
    
    protected abstract bool WaitJumpBack();
    

    protected virtual void OnTransition() { }
}