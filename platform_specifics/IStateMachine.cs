public interface IStateMachine {
    void RunFSM();
    void RunFSM(float delayRate);
    float TimeInState();
    void Reset();
}
