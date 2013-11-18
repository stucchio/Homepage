from pylab import *
from numpy import *
from numpy.linalg import solve
from scipy.integrate import odeint
from scipy.stats import norm, uniform, beta
from scipy.special import jacobi

a = 0.0
b = 3.0
theta=1.0
sigma=sqrt(theta/(2*(a+b+2)))

def eigenvalue(n):
    return theta*n*(n+a+b+1)/(a+b+2)

gaussian_var = norm()
def dW(dt):
    return norm.rvs() / sqrt(dt)

def random_walk(y0, tmax, dt, times = None):
    def rhs(y,t):
        return -theta*(y-(a-b)/(a+b+2)) + sqrt(2*theta*(1-y*y)/(a+b+2))*dW(dt)
    if (times is None):
        times = arange(0,tmax,dt)
    y = zeros(shape=times.shape, dtype=float)
    y[0] = y0
    for i in range(1,y.shape[0]):
        y[i] = y[i-1] + rhs(y[i-1], times[i])*dt
        if abs(y[i]) > 1:
            y[i] = y[i] / abs(y[i])
    return (times, y)

def make_first_set_of_plots():
    N = 1000
    x = zeros(shape=(N,), dtype=float)
    t = None
    tmax = 10
    axis([0,tmax,0,1])
    for i in range(N):
        t, y = random_walk(0.25, tmax, 0.01, t)
        x[i] = y[-1]
        if (i < 3):
            plot(t, (y+1)/2.0)

    xlabel("time")
    ylabel("CTR")
    savefig("random_walk.png")

    clf()
    subplot(211)
    hist((x+1)/2, bins=50)
    ylabel("Monte carlo results")

    subplot(212)
    best_fit = beta.fit((x+1)/2, floc=0, fscale=1)

    print best_fit
    ctr = arange(0,1,0.001)
    plot(ctr, beta(1,4).pdf(ctr), label="Invariant distribution, beta(1,4)")
    plot(ctr, beta(best_fit[0],best_fit[1]).pdf(ctr), label="Best fit, beta("+str(best_fit[0]) + "," + str(best_fit[1]) + ")")
    xlabel("CTR at t="+str(tmax))
    ylabel("pdf")
    legend()
    savefig("long_term_random_walk_result.png")

def beta(s, f):
    return poly1d(ones(shape=(s,)), True)*poly1d(-1*ones(shape=(f,)), True)

def poly_to_jacobi(x):
    """x is a poly1d object"""
    xc = x.coeffs
    N = x.order+1
    matrix = zeros(shape=(N,N), dtype=float)
    for i in range(N):
        matrix[N-i-1:N, i] = jacobi(i,a,b).coeffs
    return solve(matrix, xc)

def jacobi_to_poly(x):
    result = poly1d([0])
    for i in range(x.shape[0]):
        result = result + jacobi(i,a,b)*x[i]
    return result

def propagate_jacobi(pc, t):
    """Takes jacobi coefficients and propagates them"""
    n = arange(pc.shape[0], dtype=float)
    l = theta*n*(n+a+b+1.0)/(a+b+2.0)
    return exp(-l*t)*pc

def pde_solve(prior, t):
    result = zeros(shape=(prior.shape[0], t.shape[0]), dtype=float)
    result[:,0] = prior
    for i in range(1,t.shape[0]):
        result[:,i] = propagate_jacobi(result[:,i-1], t[i]-t[i-1])
    return result

prior = beta(3,10)
prior_in_jacobi = poly_to_jacobi(prior)
imshow(pde_solve(prior_in_jacobi, arange(0,3,0.1)))
show()
