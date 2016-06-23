import java.util.Calendar;
public abstract class AbstractHLSM extends Thread {
	protected long delayRate = 100;
    protected abstract void runHLSM( );
    public long transitionedAt = 0;
    public void run() {
        runHLSM( );
    }
    protected void pause(long delayRate) {
    	try {
			Thread.sleep( delayRate );
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
    }
    protected long timeInState() {
    	return Calendar.getInstance().getTimeInMillis() - transitionedAt;
    }
    
}