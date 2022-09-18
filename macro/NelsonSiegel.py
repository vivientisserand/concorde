import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from scipy.optimize import minimize
plt.style.use('ggplot')

class NelsonSiegel:
    def __init__(self, yields, dates):
        self.yields = yields
        self.dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]
        
    def compute_ns_value(self, lamb, beta_0, beta_1, beta_2, date):
        """From the original paper."""
        tenor_in_years = (date - datetime.now()).days / 365.25
        exp_decay = np.exp(-tenor_in_years/lamb)
        factor  = (1 - exp_decay) / (tenor_in_years/lamb)
        return beta_0 + beta_1*factor + beta_2*(factor - exp_decay)
    
    def objective(self, params):
        """L^2 distance between the model and the actual data."""
        square_error = 0.
        for (y, d) in zip(self.yields, self.dates):
            ns_pred = self.compute_ns_value(params[0], params[1], params[2], params[3], d)
            square_error += (ns_pred - y)**2
        return square_error
            
    def find_parameters(self):
        """Several accuracy and speed tests have been made and the Nelder-Mead heuristics
        appeared as a good method to best address the problem.
        The starting point coordinates come from the qualitative interpreatation of the model's
        parameters (long, middle and short term) and the literature, see the - future - 
        documentation..."""
        starting_point = [3., self.yields[-1], self.yields[len(self.yields)//2], self.yields[0]]
        result = minimize(self.objective, starting_point, method='nelder-mead')
        solution = result['x']
        return solution
    
    def discount(self, date):
        """We usually want the discount factor from this interpolation. Given a date, this method
        will return the discount factor associated. We assume continuous compounding."""
        date = datetime.strptime(date, '%Y-%m-%d')
        params = self.find_parameters()
        interpolated_yield = self.compute_ns_value(params[0], params[1], params[2], params[3], date)
        tenor_in_years = (date - datetime.now()).days / 365.25
        return np.exp(- interpolated_yield * tenor_in_years)
        
    
    def plot(self):
        """Scatter plots the data and the Nelson-Siegel fit to it."""
        date_range = pd.date_range(start = datetime.now(), end = self.dates[-1] + timedelta(days = 300), periods=1000)
        params = self.find_parameters()
        fig, ax = plt.subplots()
        ax.scatter(self.dates, self.yields)
        ax.plot(date_range, [self.compute_ns_value(params[0], params[1], params[2], params[3], d) for d in date_range])
