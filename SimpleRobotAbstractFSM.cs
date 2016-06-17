using UnityEngine;
using System.Collections;
public abstract class SimpleRobotAbstractFSM : AbstractFSM {
    protected const int IDLE = 0;
    protected const int WAITFORSECONDPRESS = 1;
    protected const int TESTMOTORS = 2;
    protected const int TESTPID = 3;
    protected int state = IDLE;
    protected int prevState = state;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) {
            prevState = state;
            // The following switch statement handles the HLSM's state action logic
            switch(state) {
                case IDLE:
                    yield return ExecuteActionIdle();
                    break;
                case WAITFORSECONDPRESS:
                    yield return ExecuteActionWaitForSecondPress();
                    break;
                case TESTMOTORS:
                    yield return ExecuteActionTestMotors();
                    break;
                case TESTPID:
                    yield return ExecuteActionTestPID();
                    break;
            }
            // The following switch statement handles the HLSM's state transition logic
            switch(state) {
                case IDLE:
                    if ( buttonPress() ) {
                        state = WAITFORSECONDPRESS;
                    }
                    break;
                case WAITFORSECONDPRESS:
                    if ( buttonPress() ) {
                        state = TESTMOTORS;
                    }
                    if ( wait() ) {
                        state = TESTPID;
                    }
                    break;
                case TESTMOTORS:
                    if ( buttonPress() ) {
                        state = IDLE;
                    }
                    break;
                case TESTPID:
                    if ( buttonPress() ) {
                        state = IDLE;
                    }
                    break;
            }
            yield return new WaitForSeconds( delayRate );
            if ( prevState!=state ) {
                transitionedAt = Time.time;
            }
        }
    }
    protected abstract IEnumerator ExecuteActionIdle();
    protected abstract IEnumerator ExecuteActionWaitForSecondPress();
    protected abstract IEnumerator ExecuteActionTestMotors();
    protected abstract IEnumerator ExecuteActionTestPID();
    protected abstract bool buttonPress();
    protected abstract bool wait();
}