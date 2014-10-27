#Pkg.add("Optim")
using Optim

function logLikelihood(z::Float64, clicks::Array{Float64,1}, shows::Array{Float64,1}, alpha::Array{Float64,1})
    @assert size(clicks) == size(shows)
    @assert size(shows) == size(alpha)
    az = z * alpha
    return sum(clicks .* log(az) .+ (shows .- clicks) .* log(1-az))
end

function derivLogLikelihood(z::Float64, clicks::Array{Float64,1}, shows::Array{Float64,1}, alpha::Array{Float64,1})
    @assert size(clicks) == size(shows)
    @assert size(shows) == size(alpha)
    az = z*alpha
    return sum((clicks / z) .- alpha .* (shows .- clicks) ./ (1 .- (alpha*z)))
end

function adQuality(clicks::Array{Int64,1}, shows::Array{Int64,1}, alpha::Array{Float64,1})
    return adQuality(map( x -> convert(Float64, x), clicks), map(x -> convert(Float64, x), shows), alpha)
end

function adQuality(clicks::Array{Float64,1}, shows::Array{Float64,1}, alpha::Array{Float64,1})
    function yToZ(y::Float64)
        return 0.5+atan(y)/pi
    end

    function dzdy(y::Float64)
        return (1.0/pi)/(1+y*y)
    end

    function zToY(z::Float64)
        return tan(pi*z-(pi/2.0))
    end

    function f(y::Array{Float64,1})
        #Uses transformed variables
        return -1*logLikelihood(yToZ(y[1]), clicks, shows, alpha)
    end

    function df!(y::Array{Float64,1}, storage::Array{Float64,1})
        storage[1] = -1 * derivLogLikelihood(yToZ(y[1]), clicks, shows, alpha) * dzdy(y[1])
    end

    result = optimize(f, df!, [0.0], method = :gradient_descent)
    return yToZ(result.minimum[1])
end

alpha = [1.0, 1.0, 1.0, 1.0]
clicks = [25,25,25,25]
shows = [100,100,100,100]

println("MLE estimated probability: ", string(adQuality(clicks, shows, alpha)))
