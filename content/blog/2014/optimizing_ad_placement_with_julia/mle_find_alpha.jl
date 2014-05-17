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

function betaToAlpha(beta::Array{Float64,1})
    result = Array(Float64, size(beta)[1] + 1)
    result[1] = 1.0
    result[2:] = cumprod(beta)
    return result
end

function gradBetaLogLikelihood(z::Array{Float64,1}, clicks::Array{Int64,2}, shows::Array{Int64,2}, beta::Array{Float64,1})
    alpha = betaToAlpha(beta)
    M, N = size(clicks)
    @assert size(z) == (M,)
    @assert size(alpha) == (N,)
    result = Array(Float64, N-1)

    for k=2:N
        for i=k:N
            for j=1:M
                result[k-1] += clicks[j,i] / beta[k-1] - (shows[j,i] - clicks[j,i]) * z[j] * (alpha[i] / beta[k-1]) / (1 - alpha[i]*z[j])
            end
        end
    end
    return result
end

function gradZLogLikelihood(z::Array{Float64,1}, clicks::Array{Int64,2}, shows::Array{Int64,2}, alpha::Array{Float64,1})
    M, N = size(clicks)
    result = Array(Float64, M)
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
        z = map(yToZ, y[1:M])
        beta = map(yToZ, y[M+1:M+N-1])
        alpha = betaToAlpha(beta)
        return -1*logLikelihood(z, clicks, shows, alpha)
    end

    function df!(y::Array{Float64,1}, storage::Array{Float64,1})
        z = map(yToZ, y[1:M])
        beta = map(yToZ, y[M+1:M+N-1])
        alpha = betaToAlpha(beta)
        storage[1:M] = -1*gradZLogLikelihood(z, clicks, shows, alpha) .* map(dzdy, y[1:M])
        gb = gradBetaLogLikelihood(z, clicks, shows, beta)
        storage[M+1:M+N-1] = -1*gradBetaLogLikelihood(z, clicks, shows, beta) .* map( dzdy, y[M+1:M+N-1])
    end
    init = Array(Float64, M+N-1)
    init[:] = 0.0
    result = optimize(f, df!, init, method = :gradient_descent)
    resultUntransformed = map( yToZ, result.minimum)
    alpha = betaToAlpha(resultUntransformed[M+1:M+N-1])
    z = resultUntransformed[1:M]
    return (alpha, z)
end

clicks = [ 25 13 10; 20 9 4; 10 4 1; 12 4 0]
shows = [ 100 105 97; 99 103 96; 102 100 101; 103 101 107]

println(computeAlphaZ(clicks, shows))

(alpha, z) = computeAlphaZ(clicks, shows)
