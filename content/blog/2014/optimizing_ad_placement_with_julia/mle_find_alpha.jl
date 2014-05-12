#Pkg.add("Optim")
using Optim


function logLikelihood(z::Array{Float64,1}, clicks::Array{Int64,2}, shows::Array{Int64,2}, alpha::Array{Float64,1})
    M, N = size(clicks)

    @assert size(z) == (M,)
    @assert size(shows) == (M,N)
    @assert size(alpha) == (N,)

    result = 0.0

    for i=1:N
        for j=1:M
            result += clicks[j,i] * log(alpha[i]*z[j]) + (shows[j,i]-clicks[j,i])*log(1-alpha[i]*z[j])
        end
    end
    return result
end

function gradAlphaLogLikelihood(z::Array{Float64,1}, clicks::Array{Int64,2}, shows::Array{Int64,2}, alpha::Array{Float64,1})
    M, N = size(clicks)
    @assert size(z) == (M,)
    @assert size(alpha) == (N,)
    result = Array(Float64, N)
    alpha[1] = 1.0
    for j=1:M
        result +=  (slice(clicks, j,:) ./ alpha)  .- (slice(shows, j,:) .- slice(clicks, j,:)) .* alpha ./ (1 .- alpha * z[j])
    end
    return result
end

function gradZLogLikelihood(z::Array{Float64,1}, clicks::Array{Int64,2}, shows::Array{Int64,2}, alpha::Array{Float64,1})
    M, N = size(clicks)
    result = Array(Float64, M)
    alpha[1] = 1.0
    for i=1:N
        result += ( (slice(clicks, :, i) ./ z)  .- (((slice(shows, :, i) .- slice(clicks, :, i)) .* alpha[i]) ./ (1 .- alpha[i] * z)) )
    end
    return result
end

function computeAlphaZ(clicks::Array{Int64,2}, shows::Array{Int64,2})
    M, N = size(clicks)

    function yToZ(y::Float64)
        return 0.5+atan(y)/pi
    end

    function dzdy(y::Float64)
        return (1+y*y) / pi
    end

    function zToY(z::Float64)
        return tan(pi*z-(pi/2.0))
    end

    # Here the y-variable is an M+N-dimensional Array{Float64,1} the first N represent transformed
    # alpha, the remainder represent transformed z
    function f(y::Array{Float64,1})
        alpha = map(yToZ, y[1:N])
        alpha[1] = 1.0
        z = map(yToZ, y[N+1:N+M])
        return -1*logLikelihood(z, clicks, shows, alpha)
    end

    function df!(y::Array{Float64,1}, storage::Array{Float64,1})
        alpha = map(yToZ, y[1:N])
        alpha[1] = 1.0
        z = map(yToZ, y[N+1:N+M])
        storage[1:N] = -1*gradAlphaLogLikelihood(z, clicks, shows, alpha) .* map( dzdy, y[1:N])
        storage[N+1:N+M] = -1*gradZLogLikelihood(z, clicks, shows, alpha) .* map(dzdy, y[N+1:N+M])
        storage[1] = 0.0
    end
    init = Array(Float64, M+N)
    init[:] = 0.0
    result = optimize(f, df!, init, method = :gradient_descent)
    resultUntransformed = map( yToZ, result.minimum)
    alpha = resultUntransformed[1:N]
    alpha[1] = 1.0
    z = resultUntransformed[N+1:N+M]
    return (alpha, z)
end

clicks = [ 25 13 10; 20 9 4; 10 3 0; 12 4 1]
shows = [ 100 105 97; 99 103 96; 102 100 101; 103 101 107]
z = [0.25, 0.2, 0.1, 0.1]
alpha = [1.0, 0.5, 0.25]

println(computeAlphaZ(clicks, shows))
