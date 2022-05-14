#!/usr/bin/env python
# coding:utf-8


import numpy as np
from scipy.optimize import leastsq


# 二次函数的标准形式
def func(params, x):
    a, b, c = params
    return a * x * x + b * x + c


# 误差函数，即拟合曲线所求的值与实际值的差
def error(params, x, y):
    return func(params, x) - y


# 对参数求解
def solveParameter(X, Y):
    p0 = np.array([10, 10, 10])
    Para = leastsq(error, p0, args=(X, Y))
    return Para


# 返回a, b, c
def getRegression(X, Y):
    Para = solveParameter(X, Y)
    return Para[0]
