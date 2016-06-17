using UnityEngine;
using System.Collections;
public abstract class BoxAITestAbstractFSM : AbstractFSM {
    protected const int INIT = 0;
    protected const int MOVEFORWARD = 1;
    protected const int TURN = 2;
    protected const int SCAN = 3;
    protected const int CHECKRANGE = 4;
    protected const int JUMPBACK = 5;
    protected const int MOVETOWARDSTARGET = 6;
    protected int state = INIT;
    protected int prevState = state;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) {
            prevState = state;
            // The following switch statement handles the HLSM's state action logic
            switch(state) {
                case INIT:
                    yield return ExecuteActionInit();
                    break;
                case MOVEFORWARD:
                    yield return ExecuteActionMoveForward();
                    break;
                case TURN:
                    yield return ExecuteActionTurn();
                    break;
                case SCAN:
                    yield return ExecuteActionScan();
                    break;
                case CHECKRANGE:
                    yield return ExecuteActionCheckRange();
                    break;
                case JUMPBACK:
                    yield return ExecuteActionJumpBack();
                    break;
                case MOVETOWARDSTARGET:
                    yield return ExecuteActionMoveTowardsTarget();
                    break;
            }
            // The following switch statement handles the HLSM's state transition logic
            switch(state) {
                case INIT:
                    break;
                case MOVEFORWARD:
                    if ( !CanSeeTarget() ) {
                        state = MOVEFORWARD;
                    }
                    break;
                case TURN:
                    if ( Wait() ) {
                        state = TURN;
                    }
                    break;
                case SCAN:
                    if ( Wait() ) {
                        state = SCAN;
                    }
                    break;
                case CHECKRANGE:
                    if ( CanSeeTarget() ) {
                        state = CHECKRANGE;
                    }
                    break;
                case JUMPBACK:
                    if ( DistLt3() ) {
                        state = JUMPBACK;
                    }
                    break;
                case MOVETOWARDSTARGET:
                    if ( !DistLt3() ) {
                        state = MOVETOWARDSTARGET;
                    }
                    break;
            }
            yield return new WaitForSeconds( delayRate );
            if ( prevState!=state ) {
                transitionedAt = Time.time;
            }
        }
    }
    protected abstract IEnumerator ExecuteActionInit();
    protected abstract IEnumerator ExecuteActionMoveForward();
    protected abstract IEnumerator ExecuteActionTurn();
    protected abstract IEnumerator ExecuteActionScan();
    protected abstract IEnumerator ExecuteActionCheckRange();
    protected abstract IEnumerator ExecuteActionJumpBack();
    protected abstract IEnumerator ExecuteActionMoveTowardsTarget();
    protected abstract bool CanSeeTarget();
    protected abstract bool DistLt3();
    protected abstract bool Wait();
}