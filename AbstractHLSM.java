public abstract class AbstractHLSM extends Thread {
    protected abstract void runHLSM( long delayRate );
    public long transitionedAt = 0;
    public void run() {
        
    }
}