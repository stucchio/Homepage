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

def grid_inst():
    xlabel("time")
    ylabel("money")
#    xticks([5], ["customer_acquisition"])
    xticks([])
    ylim([1.05*profit.min(), 1.05*max( cost.max(), revenue.max() )])
    yticks([0], "0")

#First picture
t = arange(0, 100)

cost, revenue, profit = customer_cash_flow(t, 0)

subplot(231)

title("revenue")
plot(t, revenue, label="revenue", color='b')
grid_inst()

subplot(232)

title("cost")
plot(t, cost, label="cost", color='r')
grid_inst()

subplot(233)
title("profit")
plot(t, profit, label="profit", color='g')
grid_inst()

axhline(0, color='k')

subplot(212)

title("Cumulative cash flow over time, 1 customer")
plot(t, cumsum(cost), label="cost", color='r')
plot(t, cumsum(revenue), label="revenue", color='b')
plot(t, cumsum(profit), label="profit", color='g')

legend()

xlabel("time")
xticks([5], ['customer acquisition'])
yticks([])
ylabel("money")
axhline(0, color='k')

#show()
#sys.exit(-1)
clf()

t = arange(100)

cost = zeros(t.shape, dtype=float)
revenue = zeros(t.shape, dtype=float)
profit = zeros(t.shape, dtype=float)

for i in range(0,100, 1):
    print str(i) + " is "
    c, r, p = customer_cash_flow(t, i)
    cost += c
    revenue += r
    profit += p


subplot(231)

title("revenue")
plot(t, revenue, label="revenue", color='b')
grid_inst()

subplot(232)

title("cost")
plot(t, cost, label="cost", color='r')
grid_inst()

subplot(233)
title("profit")
plot(t, profit, label="profit", color='g')
grid_inst()

axhline(0, color='k')

subplot(212)

title("Cumulative cash flow over time, constant rate of customer acquisition")
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
