#!/usr/bin/python

from pylab import *
from datetime import date, timedelta

time = array([date(2012, 1, 1), date(2012, 3,1), date(2012, 6, 1), date(2012, 9, 1), date(2013, 1,1), date(2013, 3, 1), date(2014, 1, 1), date(2014, 3, 1), date(2015, 1,1), date(2015, 3, 1), date(2015,6,1), date(2016, 1, 1), date(2016, 3,1), date(2016,6,1) ])
revenue = array([1.4, 2.1, 4.3, 8.3, 12.9, 19.3, 46.0, 57.0,  287.3, 375.9, 701.0, 960.0, 1100.0,1700.0])
cost =    array([2.6, 3.9, 5.0, 8.6, 10.3, 14.9, 97.0, 164.0, 231.9, 588.9, 697.0, 520, 750.0, 2200.0 ])


subplot(131)

title("revenue")
plot(time, revenue, 'bo')
ylim([min(revenue-cost)*1.05, max(revenue.max(), cost.max())*1.05])
xlim([time[0], time[-1]+timedelta(days=90)])
xticks([date(2012, 1, 1), date(2013, 3, 1), date(2014, 1, 1), date(2015, 1,1), date(2016, 1, 1) ])
ylabel("millions of ($)")
subplot(132)

title("cost")
plot(time, cost, 'ro')
ylim([min(revenue-cost)*1.05, max(revenue.max(), cost.max())*1.05])
xlim([time[0], time[-1]+timedelta(days=90)])
xticks([date(2012, 1, 1), date(2013, 3, 1), date(2014, 1, 1), date(2015, 1,1), date(2016, 1, 1) ])
ylabel("millions of ($)")
subplot(133)

title("profit")
plot(time, revenue - cost, 'go')
axhline(0, color='k')
ylim([min(revenue-cost)*1.05, max(revenue.max(), cost.max())*1.05])
xlim([time[0], time[-1]+timedelta(days=90)])
xticks([date(2012, 1, 1), date(2013, 3, 1), date(2014, 1, 1), date(2015, 1,1), date(2016, 1, 1) ])
ylabel("millions of ($)")

show()
clf()


subplot(131)

title("revenue")
semilogy(time, revenue, 'bo')
ylim([min(revenue-cost)*1.05, max(revenue.max(), cost.max())*1.05])
xlim([time[0], time[-1]+timedelta(days=90)])
ylabel("millions of ($)")
xticks([date(2012, 1, 1), date(2013, 3, 1), date(2014, 1, 1), date(2015, 1,1), date(2016, 1, 1) ])

subplot(132)

title("cost")
semilogy(time, cost, 'ro')
ylim([min(revenue-cost)*1.05, max(revenue.max(), cost.max())*1.05])
xlim([time[0], time[-1]+timedelta(days=90)])
ylabel("millions of ($)")
xticks([date(2012, 1, 1), date(2013, 3, 1), date(2014, 1, 1), date(2015, 1,1), date(2016, 1, 1) ])

subplot(133)

title("profit")
semilogy(time, revenue - cost, 'go', label="profit")
semilogy(time, cost - revenue, 'ro', label="loss")
legend()
ylim([min(revenue-cost)*1.05, max(revenue.max(), cost.max())*1.05])
xlim([time[0], time[-1]+timedelta(days=90)])
ylabel("millions of ($)")
xticks([date(2012, 1, 1), date(2013, 3, 1), date(2014, 1, 1), date(2015, 1,1), date(2016, 1, 1) ])

show()
