#ifndef ARDUINO_HLSM
#define ARDUINO_HLSM

#include<Arduino.h>
class BoxAITest_HLSM {
  public:
    #define INIT 0
    #define MOVEFORWARD 1
    #define TURN 2
    #define SCAN 3
    #define CHECKRANGE 4
    #define JUMPBACK 5
    #define MOVETOWARDSTARGET 6
    long transitionedAt = 0;
    uint8_t state = INIT;
    uint8_t prevState;
    void run( ) {
        prevState = state;
        // The following switch statement handles the HLSM's state action logic
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
        if ( prevState!=state ) {
            transitionedAt = millis();
        }
    }
    void ExecuteActionInit();
    void ExecuteActionMoveForward();
    void ExecuteActionTurn();
    void ExecuteActionScan();
    void ExecuteActionCheckRange();
    void ExecuteActionJumpBack();
    void ExecuteActionMoveTowardsTarget();
    bool CanSeeTarget();
    bool DistLt3();
    bool Wait();
};

#endif