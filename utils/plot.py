import matplotlib.pyplot as plt


def plot_erg_prob(ergodic_prob):
    plt.bar([x for x in range(0, len(ergodic_prob)+1)], ergodic_prob, color='blue')

    plt.title("Ergodic Probabilities")
    plt.xlabel("State")
    plt.ylabel("Probability")
    plt.show()


def plot_avg_cust(avg_cust):
    plt.plot([x for x in range(0, len(avg_cust)+1)], avg_cust)

    plt.title("Average Number of Customer in system")
    plt.xlabel("1000 transitions")
    plt.ylabel("Avg")
    plt.show()
    