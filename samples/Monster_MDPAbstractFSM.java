
public abstract class Monster_MDPAbstractFSM { 
    public enum State { 
        Idle,
        Derp,
        Roll
    }  
    public State state = State.Idle;
    protected abstract void OnTransition();
    public void Step()
    {
		State prevState = state;
            // Get a uniform random number for MDP transitions
            float rand = UnityEngine.Random.value;
		 
                switch(state) {
                    case Idle:
                        ExecuteActionIdle();
                        break;
                    case Derp:
                        ExecuteActionDerp();
                        break;
                    case Roll:
                        ExecuteActionRoll();
                        break;
            }
            // The following switch statement handles the MDP's state transition logic
            switch(state) {                case Idle:
                
                    if( WaitOneSec() ) {
                        // Probability of transition 40.0%
                        if( rand < 0.4 )
                            state = State.Roll;// Probability of transition 60.0%
                        else
                            state = State.Derp;
                    }
                    break;
                case Derp:
                
                    if( WaitOneSec() ) {
                        // Probability of transition 100.0%
                            state = State.Idle;
                    }
                    break;
                case Roll:
                
                    if( WaitOneSec() ) {
                        // Probability of transition 100.0%
                            state = State.Idle;
                    }
                    break;
            }		
		
            if (prevState != state)
            {
                OnTransition();
            }
			
    }
    // State Logic Functions
    protected abstract void ExecuteActionIdle();
    protected abstract void ExecuteActionDerp();
    protected abstract void ExecuteActionRoll();
    // Transitional Logic Functions
    protected abstract boolean WaitOneSec();
}