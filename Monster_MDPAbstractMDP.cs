using UnityEngine;
using System.Collections;
public abstract class Monster_MDPAbstractMDP : AbstractFSM {
    protected const int IDLE = 0;
    protected const int DERP = 1;
    protected const int ROLL = 2;
    protected int state = IDLE;
    protected int prevState = state;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) {
            prevState = state;
            // The following switch statement handles the state machine's action logic
            switch(state) {
                case IDLE:
                    yield return ExecuteActionIdle();
                    break;
                case DERP:
                    yield return ExecuteActionDerp();
                    break;
                case ROLL:
                    yield return ExecuteActionRoll();
                    break;
            }
            // Get a uniform random number for MDP transitions
            float rand = Random.value;
            // The following switch statement handles the MDP's state transition logic
            switch(state) {
                case IDLE:
                    if ( WaitOneSec() ) {
                        // Probability of transition: 40.0%
                        if ( rand < 0.4 ) {
                            state = ROLL;
                        }
                        // Probability of transition: 60.0%
                        else if ( rand < 1.0 ) {
                            state = DERP;
                        }
                    }
                    break;
                case DERP:
                    if ( WaitOneSec() ) {
                        // Probability of transition: 100.0%
                        if ( rand < 1.0 ) {
                            state = IDLE;
                        }
                    }
                    break;
                case ROLL:
                    if ( WaitOneSec() ) {
                        // Probability of transition: 100.0%
                        if ( rand < 1.0 ) {
                            state = IDLE;
                        }
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
    protected abstract IEnumerator ExecuteActionDerp();
    protected abstract IEnumerator ExecuteActionRoll();
    protected abstract bool WaitOneSec();
}