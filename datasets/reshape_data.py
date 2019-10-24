import numpy as np

traffic = np.load('./traffic.npy')



traffic = traffic.transpose()


np.save('./traffic.npy',traffic)
