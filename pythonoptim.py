 import scipy.optimize as optimize
import math 

# Initial weights (TODO: Look into how to improve initial guess)
guess = [0.03 for i in range(0,30)]
# Define the bounds for the variables (This could be changed based on risk apetite I guess)
bounds = [(0, 1) for i in range(0,30)]

#Defining constraints
def constraint(x):
    return [sum(x) - 1]

equality_constraint = {'type': 'eq', 'fun': constraint}

#Helper functions
def line_to_prob(x):
    if (x < 0):
        return (0-x/(0-x+100) * 100)
    else: 
        return (100/(x+100) * 100)

def calc_ep(line, prob, weight):
    if (line < 100):
        return (100/(0-line)*prob/100) * weight
    else:
        return (line/100*prob/100) * weight

def calc_el(line, prob, weight):
    if (line < 100):
        return (100/(0-line)*(100-prob)/100) * -weight
    else:
        return (line/100*(100-prob)/100) * -weight

def calc_sd(el, ep, mean):
    return math.sqrt((el-mean)* (el-mean) + (ep-mean)* (ep-mean))

def squared(s):
    return s * s

def calc_sd_sqaured_plus_weights_squared(s, w):
    return s * w

def calc_cov(sd1, w1, sd2, w2):
    return sd1 * w1 * sd2 * w2 * - 0.3

def calc_cov_helper(sd1list, w1list, sd2list, w2list):
    return [calc_cov(sd1, w1, sd2, w2) for sd1, w1, sd2, w2 in zip(sd1list, w1list, sd2list, w2list)]

def sum_nestedlist(l):
    stack = l
    total = 0
    while stack:
        elem = stack.pop()
        if type(elem) == list:
            stack.extend(elem)
        else:
            total += elem
     
    return total

#Function to minimise
def objective(vars):
    weights = [vars[x:x+10] for x in range(0, len(vars), 10)]

    lines = [[-120, 220, -700, -134, 330, -143, -275 ,-120, -223, 550],
    [325, 120, 1800 ,350 ,-143 ,320 ,650 ,280 ,500, -225],
    [250 ,240 ,650 ,275 ,320 ,320 ,400 ,280 ,375 ,350]]

    
    prob = [[line_to_prob(x) / 1.06483365 for x in sublist] for sublist in lines]
    ep = [[ calc_ep(l,p,w) for l, p, w in zip(sublist1, sublist2, sublist3)] for sublist1, sublist2, sublist3 in zip(lines, prob, weights)]
    el = [[ calc_el(l,p,w) for l, p, w in zip(sublist1, sublist2, sublist3)] for sublist1, sublist2, sublist3 in zip(lines, prob, weights)]
    mean = [[ p + l for p, l in zip(sublist1, sublist2)] for sublist1, sublist2 in zip(ep, el)]
    sd =  [[ calc_sd(l,p,m) for l, p, m in zip(sublist1, sublist2, sublist3)] for sublist1, sublist2, sublist3 in zip(ep, el, mean)]
    sd_sqared = [[squared(x) for x in sublist] for sublist in sd]
    weight_squared = [[squared(x) for x in sublist] for sublist in weights]
    sd_sqaured_plus_weights_squared= [[calc_sd_sqaured_plus_weights_squared(s,w) for s, w in zip(sublist1, sublist2)] for sublist1, sublist2 in zip(sd_sqared, weight_squared)]
    cov = []
    for i in range(0, len(sd) - 1):
        for j in range(i+1, len(sd)):
            cov.append(calc_cov_helper(sd[i], weights[i], sd[j], weights[j]))
    portfolio_ep = sum_nestedlist(mean)
    portfolio_sd = math.sqrt(sum_nestedlist(sd_sqaured_plus_weights_squared) + sum_nestedlist(cov))
    return (portfolio_sd)

result = optimize.minimize(objective, guess, bounds=bounds, constraints=equality_constraint)
cap_allocated = [x * 100 for x in result['x']]

print(result)
print(cap_allocated)
