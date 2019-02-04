import matplotlib.pyplot as plt
import numpy as np


def draw_graph(x, y, path):
    xasints = np.array(x)
    A = np.vstack([xasints, np.ones(len(xasints))]).T
    m, c = np.linalg.lstsq(A, np.array(y), rcond=None)[0]
    plt.scatter(xasints, y, color='black')
    plt.plot(xasints, m * xasints + c, color='blue')
    plt.xticks(xasints)
    plt.yticks(xasints)
    plt.title('Korrelatsioon esialgse ja pärastise koha vahel')
    plt.xlabel('Esialgne koht')
    plt.ylabel('Pärastine koht')
    plt.savefig(path)
    plt.clf()
