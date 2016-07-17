using UnityEngine;
using System.Collections;
public abstract class MonsterAbstractFSM : AbstractFSM {
    public enum State {
        Idle = 0,
        Nibble = 1,
        Scan = 2
    }  
    public State state = State.Idle;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) {
            State prevState = state;
            // The following switch statement handles the state machine's action logic
            switch(state) {
                case State.Idle:
                    yield return ExecuteActionIdle();
                    break;
                case State.Nibble:
                    yield return ExecuteActionNibble();
                    break;
                case State.Scan:
                    yield return ExecuteActionScan();
                    break;
            }
            
            // The following switch statement handles the HLSM's state transition logic
            switch(state) {
                case State.Idle:
                    if( OneSec() ) {
                        state = State.Nibble;
                    }
                    break;
                case State.Nibble:
                    if( OneSec() ) {
                        state = State.Scan;
                    }
                    break;
                case State.Scan:
                    if( TwoSec() ) {
                        state = State.Idle;
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
    protected abstract IEnumerator ExecuteActionIdle();
    
    protected abstract IEnumerator ExecuteActionNibble();
    
    protected abstract IEnumerator ExecuteActionScan();
    
    // Transitional Logic Functions
    protected abstract bool OneSec();
    
    protected abstract bool TwoSec();
    

    protected virtual void OnTransition() { }
}