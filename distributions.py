from matplotlib import pyplot as plt
import random
import numpy as np
import math
import scipy.stats as stats
def create_sample(sample_size):
    dice_throws = []
    for i in range(sample_size):
        dice_throws.append(random.randint(1,20))
    #dice_throws = stats.skewnorm().rvs(sample_size)
    return dice_throws

def expected_value(prob, possible_values):
    return np.dot(np.array(prob)[None,:],np.array(possible_values)[:,None])[0][0]

probs = [1/6, 1/6,1/6,1/6,1/6,1/6,]
values = [1,2,3,4,5,6]


def mean(values):
    sum = 0
    for i in values:
        sum += i

    return sum/len(values)

fig, axs = plt.subplots(4,3)

def show_hist(output):
    plt.xlim([1, 6])
    plt.figure("sample_size: {}".format(len(output)))
    plt.hist(output, density=False, edgecolor='white', bins=6)


def get_next_n():
    n = 0
    while True:
        yield n
        n += 1

next_num = get_next_n()
def create_sample_mean(sample_size):
    sample_means = []
    for i in range(1000):
        output = create_sample(sample_size)
        sample_means.append(mean(output))

    plt.xlim([1, 20])
    # plt.figure("sample_size: {}".format(len(output)))
    axs[next(next_num)].hist(sample_means, density=False, edgecolor='white', bins=20)



def generate_number_x():
    #return np.random.normal(1276, 1276*2, 1) #(mean, var, output)
    return stats.skewnorm(2,3)
def generate_number_y():
    #return np.random.normal(324, 324*4, 1) #(mean, var, output)
    return stats.skewnorm(2, 3)

## (skew, mean, var)
"""
r = stats.skewnorm(0,5,2).rvs(size=10000)
axs[0][0].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(100,5,2).rvs(size=10000)
axs[1][0].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(-100,5,2).rvs(size=10000)
axs[2][0].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(-1,5,2).rvs(size=10000)
axs[3][0].hist(r, density=True, histtype='stepfilled')


r = stats.skewnorm(0,5,2).rvs(size=10000)
axs[0][1].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(0,150,2).rvs(size=10000)
axs[1][1].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(0,-150,2).rvs(size=10000)
axs[2][1].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(5,10,2).rvs(size=10000)
axs[3][1].hist(r, density=True, histtype='stepfilled')

r = stats.skewnorm(0,5,2).rvs(size=10000)
axs[0][2].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(0,5,100).rvs(size=10000)
axs[1][2].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(0,5,200).rvs(size=10000)
axs[2][2].hist(r, density=True, histtype='stepfilled')
r = stats.skewnorm(5,10,10).rvs(size=10000)
axs[3][2].hist(r, density=True, histtype='stepfilled')

plt.legend(loc='best', frameon=False)
plt.show()
"""



fig_2 = plt.figure("asdf")

#data = stats.skewnorm(2, -0.1, 2.2).rvs(1)
for i in range(1000):
    ax = -2
    bx = 1200
    cx = 1200
    ay = 2
    by = 334
    cy = 900
    #plt.scatter(generate_number_x(), generate_number_y(), c='black', s = 1)
    plt.scatter(stats.skewnorm(ax, bx, cx).rvs(1), stats.skewnorm(ay, by, cy).rvs(1), c='black', s = 1)

    ax = -100
    ay = 100
    plt.scatter(stats.skewnorm(ax, bx, cx).rvs(1), stats.skewnorm(ay, by, cy).rvs(1), c='blue', s=1)

    ax = -5
    ay = 5
    plt.scatter(stats.skewnorm(ax, bx, cx).rvs(1), stats.skewnorm(ay, by, cy).rvs(1), c='green', s=1)

plt.show()