# monte-carlo
A Monte Carlo Simulation that applies the Black-Scholes-Merton Jump Diffusion model

Problem Statement:
Your client ABC is contemplating investing in a warrant issued by a biotechnology company, XYZ. XYZ is developing a potentially breakthrough pharmaceutical product that has an estimated 60% chance of succeeding and going to market. XYZ does not have revenue and its stock is currently trading at S0=$10.
The warrant is similar to a call option and expires in 1 year. The strike price is K = $10 and it can only be exercised at expiration.  How would you approach the valuation of the XYZ warrant?

A theoretical primer:
In my opinion, the main caveat to the valuation of this warrant is the development of a breakthrough product and the probability attached to it. While this case offers a numeric value attached to the success, we don’t have any information on when this breakthrough could occur. I am assuming that a successful product launch increases the price of the stock while a failed launch doesn’t cause a significant downturn.

The binomial option pricing model, while helpful in determining the value of an option at different points in time, would not work here as we don’t know at what point the trigger could occur.

The Black-Scholes-Merton formula, being an extension of the binomial lattice model, wouldn’t help model a probabilistic trigger in stock movement. The model as such is predicated on the geometric Brownian motion of stock price movement, given by the following partial differential equation:

∂S/S=r∂t+σ∂Z

Where ∂S is the change in stock price S in time ∂t, r is the risk-free interest rate, σ is the volatility of the stock and ∂Z is a Brownian motion. A limitation of this model is the assumption that the stock prices move continuously or in other words, no significant deviations take place. The Black-Scholes-Merton Jump Diffusion Model adds an element of deviation to the model and this is something we could use. This model is governed by the following partial differential equation:

∂S/S=(r-λk)∂t+σ∂Z+dJ         (1)

Where λ is the expected number of jumps during ∂t, k is the expected magnitude of the jumps and dJ is a Poisson process. A Monte Carlo Simulation would be ideal in this situation as it can model stock prices based on the above equation by factoring in the probabilistic trigger. For the purposes of this case, I will be making the assumption that only one jump will occur if the product launches and the arrival of this jump is a Poisson distribution. I will also be simulating the stock price every quarter under the assumption that the probability of the jump is equal across all 4 quarters. Therefore, if the product launch is successful, we can say that the expected number of jumps λ during a quarter is 0.25.
 
Now, assuming that the stock earns the risk-free interest rate on average, the stock price can be modelled as follows:
S_t=Se^((r-1/2 σ^2 )t+(σ√t)Z)

Where Z~N(0,1) and S_(t )is the price of the stock after time t. 

Now, we need to factor in the probabilistic trigger. In other words, if the product successfully launches, then the price of the stock can be expressed as:
S_t=x(Se^((r-1/2 σ^2 )t+(σ√t)Z) )

Henceforth, I will call the value x as the jump factor. Let us assume that α_J is the jump percentage or increase in stock price if the product successfully launches. Then the standard deviation of change in jump percent can be expressed as σ_J. By extension of our initial assumption, if the changes in jump percentage are normally distributed then the jump factor can be expressed as:
x= e^((α_J-1/2 σ_J^2 )+(σ_J W))

Where W~N(0,1). Since we are expecting the jump to occur only once, we only need one jump factor. The above equation is similar to the original compounding formula but this variable isn’t dependent on time.  If S is the pre-jump price, xS is the post jump price and the expected post jump percentage can be given by:

E((xS-S)/S)=E(S(x-1)/S)=E(x)-1=e^(α_J )-1=k

This model assumes that the percentage change in stock price is normally distributed around the risk-free interest rate which is the expected return. Now, suppose the product launches and the stock price jumps. This will affect the expected return and over time, the price will increase drastically. To prevent this, we need to adjust the expected rate of return when the stock jumps. Using equation (1), we reduce the expected return by λk and arrive at this formula:

S_t=x(Se^((r-1/2 σ^2-λk)t+(σ√t)Z) )

The picture labeled 'Stock Jump' is a sample simulation of two stock prices with the same random variables. The blue line represents the path of the stock without a jump and the green line represents the path of the stock with a jump.


                          
We can run thousands of simulations and estimate a jump 60% of the time. After performing the number of simulations needed, we can then calculate the warrant payoff of each individual simulation, take the average and discount it back at the risk-free interest rate to get an approximate present value of the warrant.

