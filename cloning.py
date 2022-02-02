import numpy
import random
import math


# defining cloning factor
def k(config, s, L, alpha):
    e = 1.0
    for i in range(L):
        if config[i % L] == 1 and config[(i+1) % L] == 0:
            e += alpha*(math.exp(s) - 1.0)/L
    return e


# defining the biased dynamics
def update(config, s, L, alpha):
    i1 = numpy.where(numpy.asarray(config) == 1)[0]  # Full slots
    i0 = numpy.where(numpy.asarray(config) == 0)[0]  # Empty slots
    movable = []
    for i in i1:
        if (i+1) % L in i0:
            # Store the location of movable particles
            movable.append(i)
    if (1-alpha*len(movable)/L)/k(config, s, L, alpha) > numpy.random.rand():
        # probability of not making a move (1PM)
        pass
    else:
        pos = numpy.random.choice(movable)  # choose a random movable particle
        config[(pos) % L] = 0
        config[(pos+1) % L] = 1
    return config


# main functionn
def main(s, alpha, T, L, M, clon):
    c = []
    c_temp = []
    m = [clon]

    # create a family of clones
    for i in range(clon):
        conf_temp = [0]*(L-M)+[1]*M
        random.shuffle(conf_temp)
        c.append(conf_temp)

    for time in range(T):

        c_temp.clear()
        # we rescale our ensemble instantly, that's why we need a counter to
        # use at the end for calculating mu
        g = 0

        for i in range(clon):
            # the agent is to be replaced by G copies
            G = int(k(c[i], s, L, alpha) + numpy.random.random())

            if G == 0:
                # one copy chosen at random replaces the current copy
                newc = random.choice([x for x in range(clon) if x != i])
                c_temp.append(c[newc])

            elif G >= 1:
                # the agent is replaced by G copies; then G-1 clones are
                # uniformly sampled out
                for _ in range(G):
                    c_temp.append(
                        update(c[i], s, L, alpha)  # do the biased dynamic
                    )
                list = random.sample(range(len(c_temp)), G-1)
                c_temp = numpy.delete(c_temp, list, axis=0)
                c_temp = c_temp.tolist()
            g += G  # keep track of the changes in the size of our ensemble

        c = c_temp.copy()
        m.append(g)

    x = [clon/m[i] for i in range(1, len(m))]
    return (-numpy.log(numpy.prod(x))/T)
