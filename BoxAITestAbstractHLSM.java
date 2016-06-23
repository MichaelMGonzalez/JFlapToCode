import java.util.Calendar;
public abstract class BoxAITestAbstractHLSM  extends AbstractHLSM {
    public final int INIT = 0;
    public final int MOVEFORWARD = 1;
    public final int TURN = 2;
    public final int SCAN = 3;
    public final int CHECKRANGE = 4;
    public final int JUMPBACK = 5;
    public final int MOVETOWARDSTARGET = 6;
    public int state = INIT;
    @Override
	protected void runHLSM( long delayRate ) {
        while(true) {
            int prevState = state;
            // The following switch statement handles the state machine's action logic
            switch(state) {
                case INIT:
                    ExecuteActionInit();
                    break;
                case MOVEFORWARD:
                    ExecuteActionMoveForward();
                    break;
                case TURN:
                    ExecuteActionTurn();
                    break;
                case SCAN:
                    ExecuteActionScan();
                    break;
                case CHECKRANGE:
                    ExecuteActionCheckRange();
                    break;
                case JUMPBACK:
                    ExecuteActionJumpBack();
                    break;
                case MOVETOWARDSTARGET:
                    ExecuteActionMoveTowardsTarget();
                    break;
            }
            // The following switch statement handles the HLSM's state transition logic
            switch(state) {
                case INIT:
                    if ( Wait() ) {
                        state = SCAN;
                    }
                    break;
                case MOVEFORWARD:
                    if ( Wait() ) {
                        state = TURN;
                    }
                    break;
                case TURN:
                    if ( Wait() ) {
                        state = SCAN;
                    }
                    break;
                case SCAN:
                    if ( CanSeeTarget() ) {
                        state = CHECKRANGE;
                    }
                    else { 
                        state = MOVEFORWARD;
                    }
                    break;
                case CHECKRANGE:
                    if ( DistLt3() ) {
                        state = JUMPBACK;
                    }
                    else { 
                        state = MOVETOWARDSTARGET;
                    }
                    break;
                case JUMPBACK:
                    if ( Wait() ) {
                        state = SCAN;
                    }
                    break;
                case MOVETOWARDSTARGET:
                    if ( Wait() ) {
                        state = SCAN;
                    }
                    break;
            }
            this.sleep( delayRate );
            if ( prevState!=state ) {
                transitionedAt = Calendar.getInstance().getTimeInMillis();
            }
        }
    }
    protected abstract void ExecuteActionInit();
    protected abstract void ExecuteActionMoveForward();
    protected abstract void ExecuteActionTurn();
    protected abstract void ExecuteActionScan();
    protected abstract void ExecuteActionCheckRange();
    protected abstract void ExecuteActionJumpBack();
    protected abstract void ExecuteActionMoveTowardsTarget();
    protected abstract boolean CanSeeTarget();
    protected abstract boolean DistLt3();
    protected abstract boolean Wait();
}