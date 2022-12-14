# -*- coding: utf-8 -*-
"""Bouston House Price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z3_6YijYyipF57HwvjHpkWIAW0pOm_xK

#Boston Housing Dataset
##Predicting Median value of owner-occupied homes

The aim of this assignment is to learn the application of machine learning algorithms to data sets. This involves learning what data means, how to handle data, training, cross validation, prediction, testing your model, etc.
This dataset contains information collected by the U.S Census Service concerning housing in the area of Boston Mass. It was obtained from the StatLib archive, and has been used extensively throughout the literature to benchmark algorithms. The data was originally published by Harrison, D. and Rubinfeld, D.L. Hedonic prices and the demand for clean air', J. Environ. Economics & Management, vol.5, 81-102, 1978.
The dataset is small in size with only 506 cases. It can be used to predict the median value of a home, which is done here. There are 14 attributes in each case of the dataset. They are:

1.CRIM - per capita crime rate by town

2.ZN - proportion of residential land zoned for lots over 25,000 sq.ft.

3.INDUS - proportion of non-retail business acres per town.

4.CHAS - Charles River dummy variable (1 if tract bounds river; 0 otherwise)

5.NOX - nitric oxides concentration (parts per 10 million)

6.RM - average number of rooms per dwelling

7.AGE - proportion of owner-occupied units built prior to 1940

8.DIS - weighted distances to five Boston employment centres

9.RAD - index of accessibility to radial highways

10.TAX - full-value property-tax rate per $10,000

11.PTRATIO - pupil-teacher ratio by town

12.B - 1000(Bk - 0.63)^2 where Bk is the proportion of blacks by town

13.LSTAT - % lower status of the population

14.MEDV - Median value of owner-occupied homes in $1000's

##Aim
###To implement a linear regression with regularization via gradient descent.
###To implement gradient descent with Lp norm, for 3 different values of p in (1,2]
###To contrast the difference between performance of linear regression Lp norm and L2 norm for these 3 different values.
###Tally that the gradient descent for L2 gives same result as matrix inversion based solution.

#Working of Code
###NumPy library would be required, so code begins by importing it
###Import phi and phi_test from train and test datasets using NumPy's loadtxt function
###Import y from train dataset using the loadtxt function
###Concatenate coloumn of 1s to right of phi and phi_test
###Apply min max scaling on each coloumn of phi and phi_test
###Apply log scaling on y
###Define a function to calculate change in error function based on phi, w and p norm
###Make a dictionary containing filenames as keys and p as values
###For each item in this dictionary
###Set the w to all 0s
###Set an appropriate value for lambda and step size
###Calculate new value of w
###Repeat steps until error between consecutive ws is less than threshold
###Load values of id from test data file
###Calculate y for test data using phi test and applying inverse log
###Save the ids and y according to filename from dictionary
"""

import numpy as np

# Import phi from train data set
phi = np.loadtxt('train1.csv', dtype='float', delimiter=',', skiprows=1,
                 usecols=tuple(range(1, 14)))

# Import y from train data set
y = np.loadtxt('train1.csv', dtype='float', delimiter=',', skiprows=1,
               usecols=14, ndmin=2)

# Import phi_test from test data set
phi_test = np.loadtxt('test.csv', dtype='float', delimiter=',',
                      skiprows=1, usecols=tuple(range(1, 14)))


# Add a cloloumn of 1s to right of phi and phi_test
phi_test = np.concatenate((phi_test, np.ones((105, 1))), axis=1)
phi = np.concatenate((phi, np.ones((400, 1))), axis=1)

# Min Max scaling for phi and phi_test (Feature Engineering)
for i in range(0, 13):
    col_max = max(phi[:, i])
    col_min = min(phi[:, i])
    phi[:, i] = (phi[:, i] - col_min) / (col_max - col_min)
    phi_test[:, i] = (phi_test[:, i] - col_min) / (col_max - col_min)

# Log scaling on y
y = np.log(y)


# Function to calculate change in error function
def delta_w(p, phi, w):
    if p == 2:
        deltaw = (2 * (np.dot(np.dot(np.transpose(phi), phi), w) -
                       np.dot(np.transpose(phi), y)) +
                  lambd * p * np.power(np.absolute(w), (p - 1)))
    if p < 2 and p > 1:
        deltaw = (2 * (np.dot(np.dot(np.transpose(phi), phi), w) -
                       np.dot(np.transpose(phi), y)) +
                  lambd * p * np.power(np.absolute(w), (p - 1)) * np.sign(w))
    return deltaw


# Dictionary containing filenames as keys and p as values
filenames = {'output.csv': 2.0,
             'output_p1.csv': 1.75,
             'output_p2.csv': 1.5,
             'output_p3.csv': 1.3
             }

# For each item in this dictionary
for (fname, p) in filenames.items():
    # Set initial w to zeros
    w = np.zeros((14, 1))

    # Hyperparameter lambda value
    lambd = 0.2

    # Maximum step size
    t = 0.00012

    # Calculate new value of w
    w_new = w - t * delta_w(p, phi, w)

    i = 0
    # Repeat steps until error between consecutive w is less than threshold
    while(np.linalg.norm(w_new-w) > 10 ** -10):
        w = w_new
        w_new = w - t * delta_w(p, phi, w)
        i = i + 1

    # Load values of id
    id_test = np.loadtxt('test.csv', dtype='int', delimiter=',',
                         skiprows=1, usecols=0, ndmin=2)

    # Calculate y for test data
    y_test = np.exp(np.dot(phi_test, w_new))

    # Save the ids and y
    np.savetxt(fname, np.concatenate((id_test, y_test), axis=1),
               delimiter=',', fmt=['%d', '%f'], header='ID,MEDV', comments='')