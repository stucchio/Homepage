using PyPlot

function em_exact(a, b, c, d)
    total = 0.0
    for i = 0:(c-1)
        total += exp(lbeta(a+i, d+b) - log(d+i) - lbeta(1+i, d) - lbeta(a, b))
    end
    return total
end

function exact(N, phi, psi)
    return em_exact(N*psi+1, N*(1-psi)+1, N*phi+1, N*(1-phi)+1)
end

function asymptotic(N, phi, psi)
    return 2 * exp( lbeta(N*(phi+psi)+2, N*(2-phi-psi)+2) - lbeta(N*phi+1, N*(1-phi)+1) - lbeta(N*psi+1, N*(1-psi)+1) ) / (N*(psi-phi))
end

function ratio(N, phi, psi)
    return exact(N, phi, psi) / asymptotic(N, phi, psi)
end


phi = 0.2
psi = 0.25

nmax = 10000
step = 100
n = int(nmax / step)

N = Array(Float64, (n,))
r1 = Array(Float64, (n,))
r2 = Array(Float64, (n,))
r3 = Array(Float64, (n,))
r4 = Array(Float64, (n,))
for i = 1:n
    N[i] = i*step
    r1[i] = ratio(N[i], 0.2, 0.25)
    r2[i] = ratio(N[i], 0.1, 0.20)
    r3[i] = ratio(N[i], 0.03, 0.06)
    r4[i] = ratio(N[i], 0.01, 0.015)
end

semilogy(N, abs(r1-1), label="\$ \\phi=0.2, \\psi=0.25\$")
semilogy(N, abs(r2-1), label="\$ \\phi=0.1, \\psi=0.20\$")
semilogy(N, abs(r3-1), label="\$ \\phi=0.03, \\psi=0.06\$")
semilogy(N, abs(r4-1), label="\$ \\phi=0.01, \\psi=0.015\$")
legend()
xlabel("N")
ylabel("Exact / Asymptotic")
savefig("asymptotic_errors.png")
