# TODO: create random time intervals for poisson events in a minute following expo distribution

import bisect
import queue
import random
import numpy as np


class Transitions:
    def __init__(self, seed, iters, queue_length):
        self.iters = iters
        self.seed = seed
        self.queue_length = queue_length

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
        trans = []
        qsize = 0
        q = queue.Queue()

        arr = arrivals.pop(0)
        cur_dep = arr + departures.pop(0)

        while len(trans) < self.iters:
            if arr<cur_dep and qsize<self.queue_length:
                if qsize > 0:
                    q.put(arr)
                qsize += 1
                trans.append(('a', arr))
                arr = arrivals.pop(0)

            elif arr<cur_dep and qsize == self.queue_length:
                trans.append(('a', arr))
                arr = arrivals.pop(0)
                continue
            elif arr >= cur_dep:
                trans.append(('d', cur_dep))

                qsize -= 1
                if qsize > 0:
                    ar = q.get()
                else:
                    ar = arr
                cur_dep = ar + departures.pop(0)
        trans = list(sorted(trans, key=lambda x: x[1]))
        return trans

    # create a state matrix
    def create_states(self, lmd, mu):
        np.random.seed(self.seed)
        seq = np.random.poisson(lmd, self.iters)
        arrivals_time = self.create_event_times(seq)
        seq_deps = np.random.exponential(1/mu,  self.iters)
        departures_intervals = [x*60 for x in seq_deps]
        transitions = self.set_transition_table(arrivals_time, departures_intervals)
        return transitions
