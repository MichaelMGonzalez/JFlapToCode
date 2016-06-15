using UnityEngine;
using System.Collections;
public abstract class MonsterAbstractFSM : MonoBehaviour {
    protected enum State { Nibble, Idle, Scan }
    State state = State.Idle;
    protected void RunFSM() {
        StartCoroutine(FSMThread());
    }
    IEnumerator FSMThread() {
        while(true) { 
            // This is the state action logic
            switch(state) {
            case State.Nibble:
                ExecuteActionNibble();
                break;
            case State.Idle:
                ExecuteActionIdle();
                break;
            case State.Scan:
                ExecuteActionScan();
                break;
            }
            // This is the state transition logic
            switch(state) {
            case State.Nibble:
                if( OneSec() )
                    state = State.Scan;
                break;
            case State.Idle:
                if( OneSec() )
                    state = State.Nibble;
                break;
            case State.Scan:
                if( TwoSec() )
                    state = State.Idle;
                break;
            }
            yield return new WaitForSeconds( delayRate );
        }
    }
    protected abstract bool OneSec();
    protected abstract bool TwoSec();
    protected abstract void ExecuteActionNibble();
    protected abstract void ExecuteActionIdle();
    protected abstract void ExecuteActionScan();
    protected float delayRate = .1f;
    protected abstract void SetDelayRate(float delayRate);
}