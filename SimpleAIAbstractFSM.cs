using UnityEngine;
using System.Collections;
public abstract class SimpleAIAbstractFSM : AbstractFSM {
    protected enum State { Slacking, Scan, Tracking, Attack, Wander, RunTowardsPlayer, Dazed, Startled, TakingDamage }
    protected State state = State.Scan;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) { 
            State prevState = state;
            // This is the state action logic
            switch(state) {
            case State.Slacking:
                yield return ExecuteActionSlacking();
                break;
            case State.Scan:
                yield return ExecuteActionScan();
                break;
            case State.Tracking:
                yield return ExecuteActionTracking();
                break;
            case State.Attack:
                yield return ExecuteActionAttack();
                break;
            case State.Wander:
                yield return ExecuteActionWander();
                break;
            case State.RunTowardsPlayer:
                yield return ExecuteActionRunTowardsPlayer();
                break;
            case State.Dazed:
                yield return ExecuteActionDazed();
                break;
            case State.Startled:
                yield return ExecuteActionStartled();
                break;
            case State.TakingDamage:
                yield return ExecuteActionTakingDamage();
                break;
            }
            // This is the state transition logic
            switch(state) {
            case State.Slacking:
                if( Wait1Sec())
                    state = State.Wander;
                break;
            case State.Scan:
                if( !SawPlayer())
                    state = State.Slacking;
                if( SawPlayer())
                    state = State.Tracking;
                break;
            case State.Tracking:
                if( !DistanceGT5())
                    state = State.Attack;
                if( DistanceGT5())
                    state = State.RunTowardsPlayer;
                break;
            case State.Attack:
                if( Wait1Sec())
                    state = State.Scan;
                break;
            case State.Wander:
                if( Wait2Sec())
                    state = State.Scan;
                if( DistLE3())
                    state = State.Startled;
                break;
            case State.RunTowardsPlayer:
                if( Wait1Sec())
                    state = State.Scan;
                break;
            case State.Dazed:
                if( Wait1Sec())
                    state = State.Scan;
                break;
            case State.Startled:
                if( Wait1Sec())
                    state = State.Tracking;
                break;
            case State.TakingDamage:
                if( Wait1Sec())
                    state = State.Dazed;
                break;
            }
            yield return new WaitForSeconds( delayRate );
            if( prevState != state ) transitionedAt = Time.time;
        }
    }
    protected abstract bool SawPlayer();
    protected abstract bool Wait2Sec();
    protected abstract bool DistLE3();
    protected abstract bool DistanceGT5();
    protected abstract bool Wait1Sec();
    protected abstract IEnumerator ExecuteActionSlacking();
    protected abstract IEnumerator ExecuteActionScan();
    protected abstract IEnumerator ExecuteActionTracking();
    protected abstract IEnumerator ExecuteActionAttack();
    protected abstract IEnumerator ExecuteActionWander();
    protected abstract IEnumerator ExecuteActionRunTowardsPlayer();
    protected abstract IEnumerator ExecuteActionDazed();
    protected abstract IEnumerator ExecuteActionStartled();
    protected abstract IEnumerator ExecuteActionTakingDamage();
}