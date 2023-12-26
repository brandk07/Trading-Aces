from optionprice import Option


# Scale down the prices for numerical stability
stock_price = 5_000_000
strike_price = 4_750_000

time_to_expiration = 10  # 10 days
annual_volatility = 20000  # This should be estimated from historical data
risk_free_rate = 0.05  # You should use the actual risk-free rate
volatility = .4
option_type = "put"

# Calculate the option cost
# option_cost = calculate_option_cost(stock_price, strike_price, time_to_expiration, annualized_volatility, risk_free_rate, option_type)

# Scale the option cost back up
# option_cost *= scale_factor

# print("Option cost:", f'{option_cost:,.2f}')
print("Option cost:")
print('European option')
some_option = Option(european=True,
                    kind=option_type,
                    s0=stock_price,
                    k=strike_price,
                    t=time_to_expiration,
                    sigma=volatility,
                    r=0.05)

print(some_option.getPrice(method="BSM",iteration=50000))
print(some_option.getPrice(method="BT"))
print(some_option.getPrice(method="MC"))
print()

option_type = "call"
some_option = Option(european=True,
                    kind=option_type,
                    s0=stock_price,
                    k=strike_price,
                    t=time_to_expiration,
                    sigma=volatility,
                    r=0.05)

print(some_option.getPrice(method="BSM",iteration=50000))
print(some_option.getPrice(method="BT"))
print(some_option.getPrice(method="MC"))

print("")
some_option = Option(european=False,
                    kind=option_type,
                    s0=stock_price,
                    k=strike_price,
                    t=time_to_expiration,
                    sigma=volatility,
                    r=0.05)

print(some_option.getPrice(method="BSM"))
print(some_option.getPrice(method="BT"))
print(some_option.getPrice(method="MC"))

# print(f'{some_option.getPrice():,.2f}')

# european	boolean	True if the option is an European option and False if it's an American one.
# kind	str	‘call’ for call option while ‘put’ for put option. Other strs are not valid.
# s0	number	initial price
# k	int	strike price
# sigma	float	volatility of stock
# r	float	risk free interest rate per annum
# [optional] dv	float	dividend rate. 0 for non-stock option, which is also the default
# [optional] t	int	length of option in days
# [optional] start	str	beginning date of the option, string like '2008-02-14',default today
# [optional] end	str	end date of the option, string like '2008-02-14',default today plus param t