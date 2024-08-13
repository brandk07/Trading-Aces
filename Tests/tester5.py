import math
import scipy.stats as stats
from optionprice import Option

def probability_of_profit(S, K, T, r, sigma, option_type, buy_price):
    # Calculate the break-even stock price
    if option_type == 'call':
        break_even = K + buy_price
    elif option_type == 'put':
        break_even = K - buy_price
    else:
        raise ValueError("Option type must be 'call' or 'put'")
    
    # Calculate the probability using the log-normal distribution
    mu = math.log(S) + (r - 0.5 * sigma**2) * T
    std_dev = sigma * math.sqrt(T)
    
    if option_type == 'call':
        # For a call option, we want P(ST > break_even)
        z_score = (math.log(break_even) - mu) / std_dev
        return 1 - stats.norm.cdf(z_score)
    else:  # option_type == 'put'
        # For a put option, we want P(ST < break_even)
        z_score = (math.log(break_even) - mu) / std_dev
        return stats.norm.cdf(z_score)

# Your existing code for setting up parameters
S = 225.15    # Current stock price
K = 75        # Strike price
T = 1        # Time to expiration (in days)
r = 0.0428      # Risk-free rate (2%)
sigma = .513   # Volatility (30%)

# Calculate current theoretical prices
call_option = Option(european=True, kind='call', s0=S, k=K, t=T, r=r, sigma=sigma)
put_option = Option(european=True, kind='put', s0=S, k=K, t=T, r=r, sigma=sigma)
call_price = call_option.getPrice(method="BSM")
put_price = put_option.getPrice(method="BSM")

print(f"Theoretical call option price: ${call_price:.2f}")
print(f"Theoretical put option price: ${put_price:.2f}")

# Calculate probability of profit
prob_call = probability_of_profit(S, K, T, r, sigma, 'call', call_price)
prob_put = probability_of_profit(S, K, T, r, sigma, 'put', put_price)

print(f"Probability of profit for call option: {prob_call:.2%}")
print(f"Probability of profit for put option: {prob_put:.2%}")