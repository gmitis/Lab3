

class Debug:
    def __init__(self, transitions):
        self.transitions = transitions

    def check_blocked(self):
        blk = 0
        a = 0
        for x in self.transitions:
            if x[0] == 'a':
                a += 1
                if a >= 11:
                    blk += 1
            else:
                a = 0
        print(f'Blocked {blk} times')

    def trace(self, i, qs, s, arr):
        print(f'\nTransition: {i + 1}\nSystem state: {qs}\nNext transition: {s}\nNumber of arrivals: {arr}')
