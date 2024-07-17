from hashlib import shake_128

p = 176857581480948244867604802349863732783663856225560523858099969581030268141874483416875345636657439749959951621
n = 176857581480948244867604802349863732783663856225560523834310386551077128936406127697123918346523659026470270500
A = 1

class prp:
    def __init__(self,state, m):
        self.state = state
        self.length = m
        self.tag = 0
        self.twsit_state = [ 76, 5, 29, 61, 62, 54, 66, 69, 81, 48,
                            20, 64, 14, 77, 50, 79, 71, 40, 93, 58, 
                            59, 19, 31, 63,  2, 96, 35, 18, 85, 56,
                            21, 33,  7, 99, 17, 38, 97, 89, 74, 32, 
                            27, 42,  3, 82, 91, 41, 86,  9, 13, 30, 
                            11, 87,  1, 88, 26, 67, 25, 75, 94, 45, 
                            68, 39, 55, 16, 28, 57, 49, 37, 52, 22, 
                            70, 36,  0,  8, 65, 72, 43, 12, 23, 53,
                            51, 60,  4, 46, 83, 90, 84, 92, 24, 15,
                            80, 98, 34, 78, 95, 44, 73, 10,  6, 47]
        self.twist()

    def next(self):
        if self.tag == self.length:
            self.tag = 0
            self.twist()
        tmp = self.state[self.tag]
        self.tag = self.tag + 1
        return tmp
    
    def twist(self):
        newstate = [self.state[self.twsit_state[i]] for i in range(100)]
        self.state = newstate


def encrypt(msg, key):
    y = shake_128("".join(map(str, key)).encode()).digest(len(msg))
    return bytes([msg[i] ^ y[i] for i in range(len(msg))])
