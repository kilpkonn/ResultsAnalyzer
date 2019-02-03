import matplotlib.pyplot as plt
import numpy as np

def draw_graph(x,y,path,color):
    xAsInts = np.array(x)
    print(xAsInts)
    A = np.vstack([xAsInts,np.ones(len(xAsInts))]).T
    m,c = np.linalg.lstsq(A,np.array(y),rcond=None)[0]
    plt.scatter(xAsInts,y)
    plt.plot(xAsInts,m*xAsInts+c, color=color)
    plt.savefig(path)