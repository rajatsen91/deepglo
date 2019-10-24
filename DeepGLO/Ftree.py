import numpy as np
import pandas as pd


class FplusTreeSampling(object):
    """
    F+ tree for sampling from a large population
    Construct in O(N) time
    Sample and update in O(log(N)) time
    """

    def __init__(self, dimension, weights=None):
        self.dimension = dimension
        self.layers = int(np.ceil(np.log2(dimension)))
        self.F = [np.array([])] * self.layers

        self.initialize(weights)

    def initialize(self, weights=None):
        """
        initialize F+ tree with uniform weights
        """
        # initialzie last layer with weights
        if weights is None:
            weight = 1.0 / self.dimension
            self.F[-1] = np.ones((self.dimension,)) * weight
        else:
            self.F[-1] = weights

        # for l in range(self.layers-2, -1 , -1):
        #    weight *= 2
        #    length = int(np.ceil(self.F[l+1].shape[0]/2.0))
        #    self.F[l] = np.ones((length,)) * weight
        #    if len(self.F[l+1])%2 != 0 :
        #        self.F[l][-1] = self.F[l+1][-1]
        #    else:
        #        self.F[l][-1] = self.F[l+1][-1] + self.F[l+1][-2]
        # assert(self.F[0][0] + self.F[0][1] == 1.0)

        for l in range(self.layers - 2, -1, -1):
            length = int(np.ceil(self.F[l + 1].shape[0] / 2.0))
            self.F[l] = np.ones((length,))
            if len(self.F[l + 1]) % 2 != 0:
                self.F[l][:-1] = self.F[l + 1][:-1].reshape((-1, 2)).sum(axis=1)
                self.F[l][-1] = self.F[l + 1][-1]
            else:
                self.F[l] = self.F[l + 1].reshape((-1, 2)).sum(axis=1)

    def print_graph(self):
        if self.dimension > 1000:
            print("Are you crazy?")
            return
        for fl in self.F:
            for prob in fl:
                print(prob, " ")
            print("||")

    def total_weight(self):
        """
        return the total weight sum
        """
        return self.F[0][0] + self.F[0][1]

    def get_weight(self, indices):
        """
        return the weight of given indices
        """
        return self.F[-1][indices]

    def sample_batch(self, batch_size):
        """
        sample a batch without replacement
        """
        indices = np.zeros((batch_size,), dtype=np.int)
        weights = np.zeros((batch_size,), dtype=np.float)
        for i in range(batch_size):
            indices[i] = self.__sample()
            weights[i] = self.F[-1][indices[i]]
            self.__update(indices[i], 0)  # wighout replacement
        self.update_batch(indices, weights)  # resume their original weights
        return indices

    def update_batch(self, indices, probs):
        """
        update weights of a given batch
        """
        for i, p in zip(indices, probs):
            self.__update(i, p)

    def __sample(self):
        """
        sample a single node, in log(N) time
        """
        u = np.random.sample() * self.F[0][0]
        i = 0
        for fl in self.F[1:]:
            # i_left = 2*i
            # i_right = 2*i +1
            if u > fl[2 * i] and fl.shape[0] >= 2 * (i + 1):  # then chose i_right
                u -= fl[2 * i]
                i = 2 * i + 1
            else:
                i = 2 * i
        return i

    def __update(self, idx, prob):
        """
        update weight of a single node, in log(N) time
        """
        delta = prob - self.F[-1][idx]

        for l in range(self.layers - 1, -1, -1):
            self.F[l][idx] += delta
            idx = idx // 2
