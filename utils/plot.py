import matplotlib.pyplot as plt


def plot_erg_prob(ergodic_prob, l):
    x = [x for x in range(0, len(ergodic_prob))]
    plt.bar(x, ergodic_prob, color='blue')

    plt.title(f'Ergodic Probabilities, lambda = {l}')
    plt.xlabel("State")
    plt.ylabel("Probability")
    plt.show()


def plot_avg_cust(avg_cust, l):
    x = [x for x in range(0, len(avg_cust))]
    plt.plot(x, avg_cust)

    plt.title(f'Average Number of Customers in system, lambda = {l}')
    plt.xlabel("1000 transitions")
    plt.ylabel("Avg")
    plt.show()
    