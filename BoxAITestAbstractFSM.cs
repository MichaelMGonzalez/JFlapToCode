using UnityEngine;
using System.Collections;
public abstract class BoxAITestAbstractFSM : AbstractFSM {
    protected enum State { MoveForward, Init, Scan, Turn, JumpBack, CheckRange, MoveTowardsTarget }
    protected State state = State.Init;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) { 
            State prevState = state;
            // This is the state action logic
            switch(state) {
            case State.MoveForward:
                yield return ExecuteActionMoveForward();
                break;
            case State.Init:
                yield return ExecuteActionInit();
                break;
            case State.Scan:
                yield return ExecuteActionScan();
                break;
            case State.Turn:
                yield return ExecuteActionTurn();
                break;
            case State.JumpBack:
                yield return ExecuteActionJumpBack();
                break;
            case State.CheckRange:
                yield return ExecuteActionCheckRange();
                break;
            case State.MoveTowardsTarget:
                yield return ExecuteActionMoveTowardsTarget();
                break;
            }
            // This is the state transition logic
            switch(state) {
            case State.MoveForward:
                if( Wait() )
                    state = State.Turn;
                break;
            case State.Init:
                if( Wait() )
                    state = State.Scan;
                break;
            case State.Scan:
                if( CanSeeTarget() )
                    state = State.CheckRange;
                if( !CanSeeTarget() )
                    state = State.MoveForward;
                break;
            case State.Turn:
                if( Wait() )
                    state = State.Scan;
                break;
            case State.JumpBack:
                if( Wait() )
                    state = State.Scan;
                break;
            case State.CheckRange:
                if( DistLt3() )
                    state = State.JumpBack;
                if( !DistLt3() )
                    state = State.MoveTowardsTarget;
                break;
            case State.MoveTowardsTarget:
                if( Wait() )
                    state = State.Scan;
                break;
            }
            yield return new WaitForSeconds( delayRate );
            if( prevState != state ) transitionedAt = Time.time;
        }
    }
    protected abstract bool CanSeeTarget();
    protected abstract bool DistLt3();
    protected abstract bool Wait();
    protected abstract IEnumerator ExecuteActionMoveForward();
    protected abstract IEnumerator ExecuteActionInit();
    protected abstract IEnumerator ExecuteActionScan();
    protected abstract IEnumerator ExecuteActionTurn();
    protected abstract IEnumerator ExecuteActionJumpBack();
    protected abstract IEnumerator ExecuteActionCheckRange();
    protected abstract IEnumerator ExecuteActionMoveTowardsTarget();
}