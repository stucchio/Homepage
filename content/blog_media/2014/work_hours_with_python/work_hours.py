from scipy.optimize import *

const = 1.0
hourly_pay = 12.0
minimum_production = 400

def production(hours_worked, num_employees):
    productivity = const * min(1.0 - 0.01 * (hours_worked-40), 1.10)
    return num_employees * hours_worked * productivity

def cost(hours_worked_pt, num_employees_pt, hours_worked_ft, num_employees_ft):
    part_time_labor_cost = hours_worked_pt * hourly_pay * num_employees_pt
    part_time_fixed_cost = 20*num_employees_pt
    full_time_labor_cost = hours_worked_ft * num_employees_ft * hourly_pay
    full_time_fixed_cost = 150*num_employees_ft
    return  (part_time_labor_cost
             + part_time_fixed_cost
             + full_time_labor_cost
             + full_time_fixed_cost)

cons = ({'type': 'ineq', 'fun': lambda x:  production(x[0], x[1]) + production(x[2],x[3]) - minimum_production},
        {'type': 'ineq', 'fun': lambda x:  x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[1]},
        {'type': 'ineq', 'fun': lambda x:  0.01 - x[0]},
        {'type': 'ineq', 'fun': lambda x:  0.01 - x[1]},
        {'type': 'ineq', 'fun': lambda x:  29-x[0]},
        {'type': 'ineq', 'fun': lambda x:  x[2] - 30},
        {'type': 'ineq', 'fun': lambda x:  x[3]},
        )

print minimize(lambda x: cost(x[0],x[1], x[2], x[3]), [25.0, 5.0, 31.0, 10.0],
               method='COBYLA',
               constraints = cons,
               options={'maxiter':5000})
