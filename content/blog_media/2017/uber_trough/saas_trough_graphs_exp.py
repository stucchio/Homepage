#!/usr/bin/python

from pylab import *
from scipy.special import erf
xkcd()

def customer_cash_flow(t, customer_acquisition_time):
    cost = zeros(t.shape, dtype=float)
    cost = (1+erf((customer_acquisition_time+10-t)/2.0))*10+1
    cost[where(t < customer_acquisition_time)] = 0.0
    revenue = zeros(t.shape, dtype=float)
    revenue[where(t >= customer_acquisition_time)] = 5
    profit = revenue - cost
    return (cost, revenue, profit)

tmax = 100
t = arange(tmax)

cost = zeros(t.shape, dtype=float)
revenue = zeros(t.shape, dtype=float)
profit = zeros(t.shape, dtype=float)

alpha = 0.05

for i in range(0,tmax, 1):
    c, r, p = customer_cash_flow(t, i)
    cost += c*exp(i*alpha)
    revenue += r*exp(i*alpha)
    profit += p*exp(i*alpha)


def grid_inst():
    xlabel("time")
    ylabel("money")
    xticks([], [])
    ylim([1.05*profit.min(), 1.05*max( cost.max(), revenue.max() )])
    yticks([0], "0")

subplot(231)
title("cost")
plot(t, cost, label="cost", color='r')
grid_inst()

subplot(232)
title("revenue")
plot(t, revenue, label="revenue", color='b')
grid_inst()

subplot(233)
title("profit")
plot(t, profit, label="profit", color='g')
axhline(0, color='k')
grid_inst()


xlabel("time")
xticks([])
ylabel("money")
axhline(0, color='k')

subplot(212)

title("Cumulative cash flow over time, exp growth, alpha = " + str(alpha))
plot(t, cumsum(cost), label="cost", color='r')
plot(t, cumsum(revenue), label="revenue", color='b')
plot(t, cumsum(profit), label="profit", color='g')

legend()

xlabel("time")
ylabel("money")
yticks([0], ['break-even'])
xticks([])
axhline(0, color='k')

show()
