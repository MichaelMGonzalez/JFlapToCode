using UnityEngine;
using System.Collections;
public abstract class SimpleAI2AbstractFSM : AbstractFSM {
    protected enum State { Scanning, Init, GoofOff, Attack }
    protected State state = State.Init;
    protected override IEnumerator FSMThread( float delayRate ) {
        while(true) { 
            State prevState = state;
            // This is the state action logic
            switch(state) {
            case State.Scanning:
                yield return ExecuteActionScanning();
                break;
            case State.Init:
                yield return ExecuteActionInit();
                break;
            case State.GoofOff:
                yield return ExecuteActionGoofOff();
                break;
            case State.Attack:
                yield return ExecuteActionAttack();
                break;
            }
            // This is the state transition logic
            switch(state) {
            case State.Scanning:
                if( DistLt5() )
                    state = State.Attack;
                if( !DistLt5() )
                    state = State.GoofOff;
                break;
            case State.Init:
                if( Wait() )
                    state = State.Scanning;
                break;
            case State.GoofOff:
                if( Wait() )
                    state = State.Scanning;
                break;
            case State.Attack:
                if( Wait() )
                    state = State.Scanning;
                break;
            }
            yield return new WaitForSeconds( delayRate );
            if( prevState != state ) transitionedAt = Time.time;
        }
    }
    protected abstract bool DistLt5();
    protected abstract bool Wait();
    protected abstract IEnumerator ExecuteActionScanning();
    protected abstract IEnumerator ExecuteActionInit();
    protected abstract IEnumerator ExecuteActionGoofOff();
    protected abstract IEnumerator ExecuteActionAttack();
}