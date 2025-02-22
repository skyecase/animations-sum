from numpy import sqrt, log, floor
import numpy as np

def flip(rate_func):
    return lambda x: 1 - rate_func(1 - x)

def in_out(rate_func):
    def func_to_return(x):
        if x < 0.5: return rate_func(2 * x) / 2
        return 1 - rate_func(2 * (1 - x)) / 2
    return func_to_return

def pow_in(order):
    return lambda x: max(0, min(x, 1)) ** order

def pow_out(order):
    return flip(pow_in(order))

quadratic_in = pow_in(2)
quadratic_out = flip(quadratic_in)
quadratic_in_out = in_out(quadratic_in)
cubic_in = pow_in(3)
cubic_out = flip(cubic_in)
cubic_in_out = in_out(cubic_in)
sqrt_in = pow_in(1/2)
sqrt_out = flip(sqrt_in)


def bounce(restitution = 1/9):
    if restitution == 0: return quadratic_in
    sqrt_restitution = sqrt(restitution)
    def func_to_return(x):
        if x >= 1: return 1
        if x <= 0: return 0
        power = floor(2 * log((1 + sqrt_restitution) * (1 - x) / 2) / log(restitution))
        return 1 - restitution ** power + ((x - 1 + restitution ** (power / 2)) * (1 + sqrt_restitution) / (1 - sqrt_restitution)) ** 2
    return func_to_return


def bounce_from_bottom(restitution = 1/9):
    if restitution == 0: return lambda x: 4 * x * (1 - x)
    sqrt_restitution = sqrt(restitution)
    def func_to_return(x):
        if x >= 1 or x <= 0: return 0
        power = floor(2 * log(1 - x) / log(restitution))
        return restitution ** power - (((x - 1) * 2 / (1 + sqrt_restitution) + restitution ** (power / 2)) * (1 + sqrt_restitution) / (1 - sqrt_restitution)) ** 2
    return func_to_return


def sin_smooth_in(linearity = 0):
    if linearity == 0:
        return lambda x: (1 - np.cos(np.pi * x)) / 2
    a = np.sqrt(linearity * (2 - linearity))
    return lambda x: 1 - np.arcsin(a * np.cos(np.pi/2 * x)) / np.arcsin(a)

def sin_smooth_out(linearity = 0): return flip(sin_smooth_in(linearity))
def sin_smooth_in_out(linearity = 0): return in_out(sin_smooth_in(linearity))