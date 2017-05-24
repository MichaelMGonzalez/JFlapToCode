
using UnityEngine;
 
namespace Mahou.Controls { 

public abstract class Hand2 : MonoBehaviour
 {
    
     
    protected float transitionedAt;
    public enum State { 
        Idle = 0,
        Start = 1,
        DetachModel = 2,
        ReattachModel = 3,
        Detached = 4
    }  
    public State state = State.Start;
    public int updateRate = 60;
    protected float timeLastTicked = 0;
    private float secondsPerStep;

    
protected virtual void OnTransition() { }

    protected void SetSecondsPerStep() {
        secondsPerStep = 1.0f/updateRate;
    }
    protected virtual void Start() {
        SetSecondsPerStep();
    }
    protected virtual void OnValidate() {
        SetSecondsPerStep();
    }
    protected float TimeInState() {
        return Time.time - transitionedAt;
    }
    protected void Update() {
        if( Time.time - timeLastTicked > secondsPerStep ) {
             MultiStep();
        }
    }

    
    public void Step()
    {
		State prevState = state;
        _Step();
        
            if (prevState != state)
            {
                transitionedAt = Time.time;
                OnTransition();
            }
        
    }
    public void MultiStep()
    {
        State prevState;
        do {
            prevState = state;
            _Step();
            if(prevState!=state) {
                transitionedAt = Time.time;
                OnTransition();
            }
        }
        while(prevState != state) ;
    }
    
    protected void _Step()
    {
		 
                switch(state) {
                    case State.Idle:
                        ExecuteActionIdle();
                        break;
                    case State.Start:
                        ExecuteActionStart();
                        break;
                    case State.DetachModel:
                        ExecuteActionDetachModel();
                        break;
                    case State.ReattachModel:
                        ExecuteActionReattachModel();
                        break;
                    case State.Detached:
                        ExecuteActionDetached();
                        break;
            }

// The following switch statement handles the HLSM's state transition logic
            switch(state) {
                case State.Idle:
                    if( ShouldDetach() ) 
                        state = State.DetachModel;
                    break;
                case State.Start:
                    state = State.Idle;
                    break;
                case State.DetachModel:
                    state = State.Detached;
                    break;
                case State.ReattachModel:
                    state = State.Idle;
                    break;
                case State.Detached:
                    if( ShouldReattach() ) 
                        state = State.ReattachModel;
                    break;
            }		
		
    }
    // State Logic Functions
    protected abstract  void ExecuteActionIdle();
    protected abstract  void ExecuteActionStart();
    protected abstract  void ExecuteActionDetachModel();
    protected abstract  void ExecuteActionReattachModel();
    protected abstract  void ExecuteActionDetached();
    // Transitional Logic Functions
    protected abstract bool ShouldReattach();
    protected abstract bool ShouldDetach();
}
 
}
