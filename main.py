# TODO: debugging code
# TODO: (debug) fix transition table: when one customer is blocked time of the rest could be wrong
# TODO: (debug) fix simulation: values not correct

import queue
from utils import plot as plt
from utils import create_transitions as ct

lmd = [1, 5, 10]
mu = 5
seed = 42
iters = 10000
queue_length = 10


# debugger
def trace(i, qs, s, arr):
    print(f'\nTransition: {i+1}\nSystem state: {qs}\nNext transition: {s}\nNumber of arrivals: {arr}\n')


# k:= index of En
# m := index that shows if we need to check for convergence
def simulate(trans):
    q = queue.Queue()
    Pn = [0] * queue_length
    Pb = 0
    En = [0] * (int(iters/1000))
    Et = 0
    qs = 0
    iter = -1
    empty_since = 0
    arrivals = 0

    for i in trans:
        iter += 1

        # trace code for debugging
        if iter < 30:
            if i[0] == 'a': arrivals += 1
            trace(iter, q.qsize(), trans[iter+1][0], arrivals)

        k = iter // 1000
        m = iter % 1000

        if i[0] == 'a' and qs < 10:
            if qs == 0:
                Pn[0] += i[1] - empty_since
            q.put(i[1])
            qs += 1
            En[k] += qs
        elif i[0] == 'a' and qs == 10:
            Pb += 1
            En[k] += qs
        elif i[0] == 'd' and qs > 0:
            if qs == 1:
                empty_since = i[1]
            wait_time = i[1] - q.get()
            Pn[qs] = wait_time
            qs -= 1
            En[k] += qs
            Et += wait_time

        if m == 0:
            En[k-1] /= 1000
            if k>1 and abs(En[k-1]-En[k-2])/En[k-2] < 0.00001:
                break

    print(f'Pn: {Pn}\nPb: {Pb}\nEn: {En}\nEt: {Et}\n')
    Pn = list(map(lambda x: x/trans[iters][1], Pn))
    return Pn, Pb/iters, En, Et


if __name__ == '__main__':
    for l in lmd:
        Trans = ct.Transitions(seed, iters, queue_length)
        transitions = Trans.create_states(l, mu)

        # debug
        blk =0
        a = 0
        for x in transitions:
            if x[0] == 'a':
                a += 1
                if a >= 11:
                    blk += 1
            else:
                a = 0
        print(f'Blocked {blk} times')
        # --debug

        ergodic_prob, p_blocking, avg_customers_in_system, avg_waiting_time = simulate(transitions)
        plt.plot_erg_prob(ergodic_prob)
        plt.plot_avg_cust(avg_customers_in_system)
