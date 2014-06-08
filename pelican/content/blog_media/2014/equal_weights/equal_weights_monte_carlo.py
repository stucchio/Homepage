from pylab import *
from numpy.random import dirichlet, rand

def _unit_weight(dim):
    return ones(dim) / float(dim)

ONE_FRAC = 0.1
def _feature_vec(dim, storage = None):
    result = rand(dim)
    result[where(result > ONE_FRAC)] = 1.0
    result[where(result <= ONE_FRAC)] = 0.0
    return result

def test_ranking(dim, nsamples=10000, h = None):
    u = _unit_weight(dim)
    if h is None:
        h = dirichlet(ones(dim))

    diff_count = 0
    zero_count = 0
    for i in range(nsamples):
        v = _feature_vec(dim)
        w = _feature_vec(dim)

        u_delta = dot(u, v-w)
        h_delta = dot(h, v-w)
        if (sign(u_delta * h_delta) < 0):
            diff_count += 1
        if u_delta == 0:
            zero_count += 1
    return ((float(diff_count) / nsamples), (float(zero_count) / nsamples))

def ranking(dim, vec_samples=100, h_samples=250):
    errors = zeros(h_samples)
    unknowns = zeros(h_samples)
    for i in range(h_samples):
        errors[i], unknowns[i] = test_ranking(dim, vec_samples)
    return (mean(errors), std(errors), mean(unknowns), std(unknowns))

if __name__=="__main__":
    n_dim = 100
    d = arange(n_dim)
    m = zeros(n_dim)
    s = zeros(n_dim)
    um = zeros(n_dim)
    us = zeros(n_dim)
    for n in range(1, n_dim):
        m[n], s[n], um[n], us[n] = ranking(n)
        print "Up to " + str(n) + " dimensions"
    plot(d, m)
    plot(d, um)

    xlabel("number of dimensions")
    ylabel("Error fraction")
    show()
