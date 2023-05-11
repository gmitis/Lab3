import bisect
import random
import numpy as np


class Transitions:
    def __init__(self, seed, iters):
        self.iters = iters
        self.seed = seed

    # calculate poisson distribution to find how many events per minute
    # calculate arrival time of x events in every minute (normal distribution is considered)
    def create_event_times(self, seq):
        new_seq = []
        minute = -1
        random.seed(self.seed)
        for i in seq:
            minute += 1
            x = 0
            while x < i:
                y = random.randint(0, 59) + 60*minute
                index = bisect.bisect_left(new_seq, y)
                new_seq.insert(index, y)
                x += 1
        return new_seq

    # creates continuous transition list with times of arrival or departure of an event
    def set_transition_table(self, arrivals, departures):
        dep_times = [x+y for x, y in zip(arrivals, departures)]
        arrivals = list(map(lambda x: ('a', x), arrivals))
        dep_times = list(map(lambda x: ('d', x), dep_times))
        trans = arrivals + dep_times
        trans = list(sorted(trans, key=lambda x: x[1]))[:self.iters]
        return trans

    # create a state matrix
    def create_states(self, lmd, mu):
        np.random.seed(self.seed)
        seq = np.random.poisson(lmd, self.iters)
        arrivals_time = self.create_event_times(seq)
        seq = np.random.exponential(1/mu,  self.iters)
        departures_intervals = [x*60 for x in seq]
        transitions = self.set_transition_table(arrivals_time, departures_intervals)
        return transitions
