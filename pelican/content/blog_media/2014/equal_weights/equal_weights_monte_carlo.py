from pylab import *
from numpy.random import dirichlet, rand, binomial, uniform

def _unit_weight(dim):
    return ones(dim) / float(dim)

ONE_FRAC = 0.5
def _feature_vec(dim):
    return binomial(1, ONE_FRAC, size=dim)
    #return uniform(0,1,dim)

def test_ranking(dim, nsamples=10000, h = None):
    u = _unit_weight(dim)
    if h is None:
        #h = dirichlet(ones(dim))
        h = zeros(dim)
        h[0] = 1.0

    diff_count = 0
    zero_count = 0

    for i in range(nsamples):
        v_minus_w =  _feature_vec(dim) - _feature_vec(dim)

        u_delta = dot(u, v_minus_w)
        h_delta = dot(h, v_minus_w)
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
#    plot(d, um)

    xlabel("number of dimensions")
    ylabel("Error fraction")
    show()
