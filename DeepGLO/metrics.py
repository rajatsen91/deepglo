import numpy as np


def smape(P, A):
    nz = np.where(A > 0)
    Pz = P[nz]
    Az = A[nz]

    return np.mean(2 * np.abs(Az - Pz) / (np.abs(Az) + np.abs(Pz)))


def mape(P, A):
    nz = np.where(A > 0)
    Pz = P[nz]
    Az = A[nz]

    return np.mean(np.abs(Az - Pz) / np.abs(Az))


def wape(P, A):
    return np.mean(np.abs(A - P)) / np.mean(np.abs(A))


def confidence_score(func, P1, A1, num):
    P = P1.flatten()
    A = A1.flatten()

    values = []

    for i in range(num):
        I = np.random.choice(len(P), int(0.63 * len(P)), replace=False)
        p = P[I]
        a = A[I]
        values += [func(p, a)]

    return np.mean(values), np.std(values)


def confidence_score_dim(func, P1, A1):
    composite = np.hstack([P1, A1])
    n, m = P1.shape

    values = np.apply_along_axis(lambda x: func(x[0:m], x[m::]), axis=0, arr=composite)

    return np.mean(values), np.std(values)
