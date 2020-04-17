



import numpy as np
import scipy.stats


def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * scipy.stats.t.ppf((1 + confidence) / 2., n-1)
    return m, m-h, m+h



data = [1, 2, 3, 4, 5]

data = [84.7, 84.9, 85.3, 85.1, 85.7]

r = mean_confidence_interval(data)


print(r)