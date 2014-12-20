title: How many hours of work is optimal? A Python Optimization tutorial
date: 2014-09-25 08:00
author: Chris Stucchio
tags: statistics, public policy, economics, optimization
category: optimization

A commonly asserted fact is that as an individual employee's working hours increase, his hourly productivity decreases. This is supported by a variety of studies. This naturally begs the question - why do employers often demand that employees work for long hours? Are employers simply irrational? In this post I'll use Python's `scipy.optimize` module to explore this question under various assumptions.

First I'll pull some numbers out of the literature. This article [reviews some estimates](http://papers.ssrn.com/sol3/papers.cfm?abstract_id=2149325) of the response of labor productivity to working hour variations. On page 9 they cite an estimate suggesting that 60 hours of work can result in a 20% drop in productivity. I'll *assume* this effect is linear, i.e. that each additional hour of work past 40 reduces hourly productivity by 1%. I'll similarly assume that productivity can be *increased* in the same way by reducing labor hours below 40.

It's important to note that most of what I'm describing applies only to commodity labor. In many skilled professions [productivity increases with hours worked](http://www.aeaweb.org/aea/2014conference/program/retrieve.php?pdfid=1103). For example, consider a trader who spends 30 hours/week understanding his strategy and another 30 hours/week running it. If he works fewer hours, his productivity drops precipitously - he's either trading a strategy he doesn't understand or learning a strategy he doesn't have time to put into practice.

# Representing it in Python

Before I begin, I want to emphasize that this is a *Python* tutorial. Most of what I'm doing here could be done more exactly and efficiently with simple calculus.

The first quantity we might think of measuring is the hourly cost of labor. So an employee who works a certain number of hours is paid in proportion to the number of hours worked. So lets do a cost/benefit analysis:

```python
productivity = const * (1.0 - 0.01 * (hours_worked-40))
production_per_employee = const * hours_worked * (1.0 - 0.01 * (hours_worked-40))
cost = hours_worked * hourly_pay
```
Now, as an employer, you need to obtain a certain amount of production - for example, you need to bake a certain number of cookies to deliver to paying customers. So lets pick some concrete numbers:

```python
const = 1.0
hourly_pay = 12.0
minimum_production = 400
```

One way to achieve this is to have 10 employees working 40 hours a week. That will cost `40 * 12 * 10 = 4800`. Is this optimal? Lets see what `scipy.optimize` says:

```python
def production(hours_worked, num_employees):
    productivity = const * (1.0 - 0.01 * (hours_worked-40))
    return num_employees * hours_worked * productivity

def cost(hours_worked, num_employees):
    return hours_worked * hourly_pay * num_employees
```

So our goal is to minimize the `cost` function. Toward that end, lets let a vector `x = [hours_worked, num_employees]` represent the two variables we have under our control.

To start we need to set up some constraints:

```python
cons = ({'type': 'ineq', 'fun': lambda x:  production(x[0], x[1]) - minimum_production},
        {'type': 'ineq', 'fun': lambda x:  x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[1]},
        )
```

The first line here tells us that `production` must be larger than `minimum_production` - i.e., we must generate at least 400 boxes of cookies. The `minimize` method, which we'll use shortly, interprets a constraint of type `"ineq"` to mean "make the `fun` argument non-negative".

The second line means that `hours_worked` cannot be negative, while the third line means that `num_employees` cannot be negative. Both of those sound like reasonable constraints to me.

Now we are ready to do some optimizing:

```python
from scipy.optimize import minimize

print minimize(lambda x: cost(x[0],x[1]), [40.0, 10.0],
               method='COBYLA',
               constraints = cons)
```

The second argument, `[40.0, 10.0]` is the *starting point* of the iteration. Since I couldn't think of anything better, I chose the normal 40 hour work week. What's the result?

```
  status: 2
    nfev: 1000
   maxcv: 0.00059420773192186971
 success: False
     fun: 3442.9141083007685
       x: array([   0.58342676,  491.76611424])
 message: 'Maximum number of function evaluations has been exceeded.'
```

That's not a helpful result. It says the program got as far as setting `hours_worked=0.58` (about 34 minutes) and `num_employees=492` but then stopped because it reached 1000 iterations. At this allocation, the cost was $3443, which is significantly cheaper than $4800.

One way to try to get an answer is to increase the maximum number of iterations:

```python
print minimize(lambda x: cost(x[0],x[1]), [0.59, 492.0],
               method='COBYLA',
               constraints = cons,
               options={'maxiter':5000})
```

```
  status: 2
    nfev: 5000
   maxcv: 0.00016903282607927395
 success: False
     fun: 3430.9145177110991
       x: array([  9.56699204e-02,   2.98849985e+03])
 message: 'Maximum number of function evaluations has been exceeded.'
```

That's even better! We got the cost down to $3431, and we have 2988 employees working 5.7 minutes each. This still isn't optimal, but it's more than $1400/week cheaper than our original allocation of 10 workers at 40 hours each.

## Time for a 5.6 minute work week?!?

The math can't be wrong. It shows that the best thing for bakery owners would be to have a 5.7 minute work week and a parade of 3000 workers passing through each week, each worker performing a single task before leaving.

So why won't the greedy capitalist bakers implement this solution, apart from the fact that it's patently ridiculous?

More concretely, how can we make the mathematics return an answer that isn't ridiculous?

# Constraining our choices

The simplest way to get a better result is to explicitly impose it. For example, suppose we believe it's utterly ridiculous for any employee to work less than 5 hours/week. Then we can impose that as a constraint on the problem:

```python
cons = ({'type': 'ineq', 'fun': lambda x:  production(x[0], x[1]) - minimum_production},
        {'type': 'ineq', 'fun': lambda x:  x[0] - 5 },
        {'type': 'ineq', 'fun': lambda x:  x[1]},
        )
```

Now we demand that `hours_worked - 5 >= 0`, or equivalently `hours_worked >= 5`. What happens?

```
  status: 1
    nfev: 449
   maxcv: 0.0
 success: True
     fun: 3555.5555555555557
       x: array([  5.        ,  59.25925926])
 message: 'Optimization terminated successfully.'
```

In that case, we achieve the optimim at 5 hours/week. If we demand that `hours_worked >= 4.3` then our optimizer will tell us employees should work 4.3 hours/week.

This is unsatisfying. After all, imposing a 5 hours/week minima is just as arbitrary as a 40 hour/week minima, and the goal of this exercise is to actually figure out the best allocation of time rather than simply arbitrarily choose it.

Another choice we might make is cap the number of employees - 49 is a good number since many regulatory hassles kick in at 50. But again, all we do is lower hours worked to 6.1, resulting in us hiring exactly 49 employees.

So time for a 6.1 hour work week?

# Per-employee costs

The key to the puzzle is to reason out *why* we find having more employees ridiculous. The idea is ridiculous because as a manager, we'll need to keep track of 49-3998 employees, depending on which model we choose.

This is a real cost. But in our simplified model we just aren't taking it into account. For example, what if it costs $20/week (account for time, payment processing costs, etc) simply to cut an employee a paycheck? In that case the cost function is:

```python
def cost(hours_worked, num_employees):
    return hours_worked * hourly_pay * num_employees + 20*num_employees
```

Now what happens when we optimize?

```
  status: 1
    nfev: 525
   maxcv: 1.1798647392424755e-08
 success: True
     fun: 4262.8199555771807
       x: array([ 13.69928819,  23.11831576])
 message: 'Optimization terminated successfully.'
```

With this change, all of a sudden we find the optimal work week is 13.7 hours. Below that and we waste too much money on payroll processing. Above that and we waste money on  With $100/week in per-employee costs (e.g., health insurance, time spent managing employees), the optimal work week rises to 27 hours.

# A more complicated model? Python's got you covered.

Of course, our assumptions are still not very realistic. First of all, we only need to pay health insurance for full time (30+ hour) employees.

Second, it's probably not realistic to assume that an employee working 20 hours/week is 20% *more productive* than one working 40 hours/week. While the productivity drop for extended working hours probably occurs, the productivity increase for low hours likely does not. So suppose productivity stops improving past 30 hours.

So lets put this into the model:

```python
def production(hours_worked, num_employees):
    productivity = const * min(1.0 - 0.01 * (hours_worked-40), 1.10)
    return num_employees * hours_worked * productivity
```

To handle part time and full time employees, lets assume we have both categories of employee and they work a different number of hours. Further suppose that part time employees have a fixed cost of $20/week, whereas full time employees have a fixed cost of $100/week.

Then our costs become:

```python
def cost(hours_worked_pt, num_employees_pt, hours_worked_ft, num_employees_ft):
    part_time_labor_cost = hours_worked_pt * hourly_pay * num_employees_pt
    part_time_fixed_cost = 20*num_employees_pt
    full_time_labor_cost = hours_worked_ft * num_employees_ft * hourly_pay
    full_time_fixed_cost = 100*num_employees_ft
    return  (part_time_labor_cost
             + part_time_fixed_cost
             + full_time_labor_cost
             + full_time_fixed_cost)
```

The $100 full time fixed cost corresponds to about $400/month per full time employee - a quick google search suggests this is a very plausible cost for health insurance alone (to say nothing of other benefits/desk space/etc).

We also need to impose extra constraints. By definition, a full time worker works at least 30 hours, and a part time worker works 29 or less. So the constraints become:

```python
cons = ({'type': 'ineq', 'fun': lambda x:  production(x[0], x[1]) + production(x[2],x[3]) - minimum_production},
        {'type': 'ineq', 'fun': lambda x:  x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[1]},
        {'type': 'ineq', 'fun': lambda x:  29-x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[2] - 30},
        {'type': 'ineq', 'fun': lambda x:  x[3]},
        )
```

According to this simulation, the optimal number of work hours is exactly 29 for part time workers (and 0 full time workers should be hired).

Of course, this effect is driven entirely by fixed costs - even if we throw away the assumption that fewer hours increases productivity, we get the same result.

# Conclusion

Python has a lot of the scientific tools you'll need already built. For tricky optimization problems like the ones above, don't guess or use heuristics. Just set up the problem exactly and let scipy do the work. There is a good chance you can find the answer you seek without too much difficulty.

On the topic of work hours and reducing the work week, let us take it as a given that shorter/longer hours reduce productivity. It does not directly follow from this fact that work hours should be reduced - in fact, the sole driver of a full time/part time decision in my models is simply the size of the fixed costs. The productivity changes do not matter much. I recognize that this conclusion will be disputed by many. I encourage anyone who disagrees (or anyone considering hiring employees) to adjust the productivity and cost functions as needed - my desire is to convey a methodology, not derive a conclusion. In practice I doubt any conclusion will be robust across industries - the features of this problem suggest it will be very sensitive to the details of the model.
