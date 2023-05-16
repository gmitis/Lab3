# TODO: debugging code
# TODO: (debug) fix transition table: when one customer is blocked time of the rest could be wrong
# TODO: (debug) fix simulation: values not correct

import queue
from functools import reduce

from utils import plot as plt
from utils import create_transitions as ct
from utils import debug as dg

lmd = [1, 5, 10]
mu = 5
seed = 42
iters = 10000
queue_length = 10


# k:= index of En
# m := index that shows if we need to check for convergence
def simulate(trans, Deb):
    q = queue.Queue()
    Pn = [0] * (queue_length+1)
    Pb = 0
    En = [0] * (int(iters/100))
    Et = 0
    qs = 0
    iter = -1

    prev_trans = 0
    arrivals = 0

    for i in trans:
        iter += 1

        # trace code for debugging
        # if iter < 30:
        #     if i[0] == 'a': arrivals += 1
        #     Deb.trace(iter, q.qsize(), trans[iter+1][0], arrivals)
        # /trace code for debugging

        k = iter // 1000
        m = iter % 1000

        if i[0] == 'a' and qs < 10:
            Pn[qs] += i[1] - prev_trans
            prev_trans = i[1]
            q.put(i[1])
            qs += 1
            En[k] += qs
        elif i[0] == 'a' and qs == 10:
            Pb += 1
            En[k] += qs
        elif i[0] == 'd' and qs > 0:
            Pn[qs] += i[1] - prev_trans
            prev_trans = i[1]
            qs -= 1
            En[k] += qs
            Et += i[1] - q.get()

        if m == 0:
            if k>1 and abs(En[k-1]-En[k-2])/En[k-2] < 0.00001:
                break

    Pn = list(map(lambda x: x/trans[iters-1][1], Pn))
    En = list(map(lambda x: x/1000, En))
    return Pn, Pb/iters, En, Et/iters


if __name__ == '__main__':
    for l in lmd:
        Trans = ct.Transitions(seed, iters, queue_length)
        transitions = Trans.create_states(l, mu)

        # debug class
        deb = dg.Debug(transitions)

        ergodic_prob, p_blocking, avg_customers_in_system, avg_waiting_time = simulate(transitions, deb)

        # debug
        print(f'\nPn: {ergodic_prob}\nPb: {p_blocking}\nEn: {avg_customers_in_system}\nEt: {avg_waiting_time}\n')
        # /debug

        plt.plot_erg_prob(ergodic_prob, l)
        plt.plot_avg_cust(avg_customers_in_system, l)
