from pylab import *
from numpy.random import dirichlet, rand, binomial, uniform, normal

def _unit_weight(dim):
    return ones(dim) / float(dim)

ONE_FRAC = 0.5
SQRT_TWO_INV = 1.0 / sqrt(2.0)
def _feature_vec(dim, method="bernoulli"):
    if method == "bernoulli":
        return binomial(1, ONE_FRAC, size=dim)
    if method == "uniform":
        return uniform(0,1,dim)
    if method == "gaussian":
        return normal(scale=SQRT_TWO_INV, size=dim)

def test_ranking(dim, nsamples=10000, h = None, feature_method="bernoulli"):
    u = _unit_weight(dim)
    if h is None:
        h = dirichlet(ones(dim))

    diff_count = 0
    zero_count = 0

    for i in range(nsamples):
        v_minus_w =  _feature_vec(dim, method=feature_method) - _feature_vec(dim, method=feature_method)

        u_delta = dot(u, v_minus_w)
        h_delta = dot(h, v_minus_w)
        if (sign(u_delta * h_delta) < 0):
            diff_count += 1
        if u_delta == 0:
            zero_count += 1
    return ((float(diff_count) / nsamples), (float(zero_count) / nsamples))

def ranking(dim, vec_samples=100, h_samples=250, feature_method="bernoulli"):
    errors = zeros(h_samples)
    unknowns = zeros(h_samples)
    for i in range(h_samples):
        errors[i], unknowns[i] = test_ranking(dim, vec_samples, feature_method=feature_method)
    return (mean(errors), std(errors), mean(unknowns), std(unknowns))

if __name__=="__main__":
    n_dim = 100
    d = arange(n_dim, dtype=float)
    bernoulli = zeros(n_dim)
    gaussian = zeros(n_dim)

    for n in range(1, n_dim):
        bernoulli[n] = ranking(n, feature_method="bernoulli")[0]
        gaussian[n] = ranking(n, feature_method="gaussian")[0]
        print "Up to " + str(n) + " dimensions"
    plot(d, bernoulli, label="Bernoulli")
#    plot(d, gaussian, label="Gaussian")
#    plot(d, 2*arctan(sqrt((d-1)/(d+1)))/(2*pi), label="theoretical gaussian bound")
#    plot(d, um)

    xlabel("number of dimensions")
    ylabel("Error fraction")
#    legend()
    show()
