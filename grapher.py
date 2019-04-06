import matplotlib.pyplot as plt
import numpy as np
import math


def draw_graph(x, y, path):
    xasints = np.array(x)
    y_ax = [x for x in range(math.ceil(max(y)) + 1)]
    A = np.vstack([xasints, np.ones(len(xasints))]).T
    m, c = np.linalg.lstsq(A, np.array(y), rcond=None)[0]
    plt.scatter(xasints, y, color='black')
    plt.plot(xasints, m * xasints + c, color='blue')
    plt.xticks([0] + x)
    plt.yticks(y_ax)
    plt.title('Korrelatsioon esialgse ja teisendatud koha vahel')
    plt.xlabel('Esialgne koht')
    plt.ylabel('Teisendatud koht')
    plt.savefig(path)
    plt.clf()
