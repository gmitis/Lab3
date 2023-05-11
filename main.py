# TODO: calculate metrics (avg customers in system)
# TODO: debugging code

import random
import numpy as np
import bisect

lmd = [1, 5, 10]
mu = 5
seed = 42
iters = 10000


# calculate poisson distribution to find how many events per minute
# calculate arrival time of x events in every minute (normal distribution is considered)
def create_event_times(seq):
    new_seq = []
    minute = -1
    random.seed(seed)
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
def set_transition_table(arrivals, departures):
    dep_times = [x+y for x, y in zip(arrivals, departures)]
    arrivals = list(map(lambda x: ('a', x), arrivals))
    dep_times = list(map(lambda x: ('d', x), dep_times))
    trans = arrivals + dep_times
    trans = list(sorted(trans, key=lambda x: x[1]))[:iters]
    print(len(trans), trans)
    return trans


# create a state matrix
def create_states(lmd, mu):
    np.random.seed(seed)
    seq = np.random.poisson(lmd, iters)
    arrivals_time = create_event_times(seq)
    seq = np.random.exponential(1/mu,  iters)
    departures_intervals = [x*60 for x in seq]
    transitions = set_transition_table(arrivals_time, departures_intervals)
    return transitions


# debugger
def trace(number_of_state_transfers):
    pass


# ergodic state probabilities of systemn
def stable_state_probabilities():
    pass


# probability of a customer being rejected cause system is full
def blocking_probability():
    pass


# average number of customers in the system
def average_customers():
    pass


# average time spent in the system by a customer
def average_time():
    pass


def simulate(trans):
    for i in trans:
        pass


if __name__ == '__main__':
    transitions = create_states(5, mu)
    simulate(transitions)




