#!/usr/bin/env python3

"""
Carrot example used in the paper.
"""

from sklearn.linear_model import LinearRegression

def price(weight, length):
    return 0.1 * weight + 0.2 * length + 2

X_a = [
    (10, 1000), 
    (-999, 1),
    (0, 0),
]
Y_a = [price(*x) for x in X_a]

model = LinearRegression()

model.fit(X_a, Y_a)

print(", ".join([f"{x:.2f}" for x in list(model.coef_) + [model.intercept_]]))