import time
class MonsterAbstractFSM:
    Idle = 0
    Nibble = 1
    Scan = 2
    def __init__(self, delay_rate=.01):
        self.delay_rate = delay_rate
        self.transitioned_at = 0
        self.state = MonsterAbstractFSM.Idle
    def run(self):
        while True:
            prevState = self.state;
            # The following switch statement handles the state machine's action logic
            if self.state == MonsterAbstractFSM.Idle:
                self.execute_action_Idle()
            elif self.state == MonsterAbstractFSM.Nibble:
                self.execute_action_Nibble()
            elif self.state == MonsterAbstractFSM.Scan:
                self.execute_action_Scan()
            # The following switch statement handles the HLSM's state transition logic
            if self.state == MonsterAbstractFSM.Idle:
                 if self.OneSec(): 
                    self.state = MonsterAbstractFSM.Nibble
            elif self.state == MonsterAbstractFSM.Nibble:
                 if self.OneSec(): 
                    self.state = MonsterAbstractFSM.Scan
            elif self.state == MonsterAbstractFSM.Scan:
                 if self.TwoSec(): 
                    self.state = MonsterAbstractFSM.Idle
            time.sleep( self.delay_rate )
            if prevState != self.state:
                self.transitioned_at = time.time
                OnTransition()
    # State Logic Functions
    def execute_action_Idle(self):
        pass
    def execute_action_Nibble(self):
        pass
    def execute_action_Scan(self):
        pass
    # Transitional Logic Functions
    def OneSec(self):
        pass
    def TwoSec(self):
        pass
    def on_transition(self):
        pass
doo = MonsterAbstractFSM()
doo.run()
