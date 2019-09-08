
import numpy as np
import math
from random import randint
import pandas as pd
stock_start = 10        # Given stock price
annual_vol = 0.70       # Given volatility
risk_free_rate = 0.02   # Given risk free interest rate
n = 4                   # 4 quarters
h = 1/n                 # Calculating stock price movement from t to t+h
num_simulations = 10000 # User defined
jump_percent = 0.15     # Assumption
jump_vol = 0.05         # Assumption
simulation_df = pd.DataFrame()            # To display output
simulation_df[0] = ['Q1','Q2','Q3','Q4','Strike price','Option payoff','Was product launch successful?']
k = math.exp(jump_percent) - 1            # Expected jump percentage
option_prices = np.empty(num_simulations) # Empty array to store option payoffs

for i in range(num_simulations):          # Start loop for number of simulations needed
    count = 0                             # Variable to keep track of number of quarters
    probability_success = randint(1,10)   # Random variable to simulate successful product launch
    Z = np.random.normal(0,1)             # To calculate the stock drift
    check=''                              # Variable to keep track of product launch success
    Lambda = 0                            # Number of jumps per quarter
    if probability_success<=6 :
        check ='Yes'
        jump_normal = np.random.normal(0,1)     
        jump_factor = math.exp((jump_percent-(0.5*jump_vol*jump_vol)) + jump_vol*jump_normal)  # As per 3(a)
        Lambda = 0.25                     # The stock price will jump 0.25 times every quarter
    else:
        jump_factor = 1                   # This factor becomes irrelevant to stock price
        check = 'No'
    price_series=[]                       # List of simulated prices for the current simulation
    factor = math.exp((risk_free_rate - (0.5*annual_vol*annual_vol) - (Lambda*k))*h + annual_vol*Z*math.sqrt(h)) # Calculation as per 3(a)
    price = stock_start * factor * jump_factor # Stock price for first quarter
    price_series.append(price)
    for j in range(n):                    # Start loop for remaining 3 quarters
        if count == n-1:                  # If we have calculated prices for all 4 quarters, then break
            break
        Z1 = np.random.normal(0,1)
        factor = math.exp((risk_free_rate - (0.5*annual_vol*annual_vol) - (Lambda*k))*h + annual_vol*Z1*math.sqrt(h)) # As per 3(a)
        if(check=='Yes'):                 # Checking to see if we need to model in the jump_factor
            jump_normal = np.random.normal(0,1)
            jump_factor = math.exp((jump_percent-(0.5*jump_vol*jump_vol)) + jump_vol*jump_normal)
        elif(check=='No'):
            jump_factor = 1
        price = price_series[count] * factor * jump_factor
        price_series.append(price)
        count+=1
    if(price_series[1]>12 or price_series[3]>14):   # If the price after 6 months is greater than $12 or if the ending price is greater than $14
        kstep = 11                                  # Then strike price = $11
    else:
        kstep = 10                                  # Else strike price = $10
    price_series.append(kstep)
    payoff = max(price_series[3]-price_series[4],0) # Calculate option payoff
    price_series.append(payoff)
    price_series.append(check)
    simulation_df[i+1] = price_series               
    option_prices[i] = payoff

option_price = ((np.sum(option_prices))/num_simulations)*(math.exp(-0.02)) # Adding up the payoffs and discounting it to the present
print(simulation_df)
print(option_price)


