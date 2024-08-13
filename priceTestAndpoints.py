# from optionprice import Option


# # Scale down the prices for numerical stability
# stock_price = 4_750_000
# strike_price = 5_000_000
from Classes.imports.optionVal import OptionVal as Op

stock_price = 239.31
strike_price = 250
time_to_expiration = 49.5  # 10 days
risk_free_rate = 0.05  # You should use the actual risk-free rate
volatility = .106
option_type = "put"


optionObj = Op(european=True,kind=option_type,s0=float(stock_price)*100,k=strike_price*100,t=time_to_expiration,sigma=volatility,r=0.05)
print(optionObj.getPrice(method="BSM",iteration=1))
# print(optionObj.getPrice(method="BT",iteration=1000))
# # stock_price = 4_050_000
# # time_to_expiration = 8
# # Calculate the option cost
# # option_cost = calculate_option_cost(stock_price, strike_price, time_to_expiration, annualized_volatility, risk_free_rate, option_type)

# # Scale the option cost back up
# # option_cost *= scale_factor

# # print("Option cost:", f'{option_cost:,.2f}')
# from collections import OrderedDict


# import timeit
# from Classes.imports.StockOption import calculate_volatility


# # mydict = {'a': 1, 'b': 2, 'c': 3}
# # start_time = timeit.default_timer()
# # mydict['d'] = 4
# # elapsed_time = timeit.default_timer() - start_time
# # print(f"Total time: {elapsed_time} seconds",mydict)

# # start_time = timeit.default_timer()
# # od = OrderedDict(mydict)
# # od.move_to_end('d', last=False)
# # elapsed_time = timeit.default_timer() - start_time
# # print(f"Total time: {elapsed_time} seconds", dict(od))

# # start_time = timeit.default_timer()

# # points = [100.0, 101.79932717000145, 105.80158425397516, 109.88219003138235, 111.5923330397885, 116.89105295364428, 109.58256268345222, 112.08421291122617, 114.17037403983522, 116.80256729083624, 118.42135546004597, 115.91536771027513, 120.01227197863867, 124.72077048241393, 122.88739434112003, 118.85934771318047, 115.01607567759257, 111.0492495119061, 109.69961087507954, 109.32072254096201, 108.23229396242307, 109.02771594537826, 110.91642245635359, 110.84227349768632, 115.42827010057823, 113.84329197733052, 114.88810013412031, 109.56194324147694, 113.07832539932974, 118.57240006741567, 111.39603724378847, 110.22616943544182, 110.82556051019316, 114.19056155052766, 112.3896680865289, 116.66586526703432, 120.06669228544179, 119.64180197052882, 118.54782872326747, 119.40609676561883, 111.70329754207053, 120.89286887706585, 119.43764571936337, 125.34591801792561, 126.18777189886023, 128.9641861027675, 136.7625088066617, 141.53934995350102, 146.4379716258795, 145.17451125177035, 146.11590846812695, 152.59294691011578, 156.49234649191752, 170.65180510660656, 165.04217870486806, 170.89222332198847, 177.3804097213149, 183.83891920634127, 186.64187244098738, 185.19037342056419, 185.74381624399027, 183.98571835047227, 184.63730665409113, 188.16273209104932, 197.55716702628956, 196.40146661092624, 203.93760330697455, 212.32471496288863, 224.84653479767775, 231.22709694755693, 237.0498443540998, 227.5163209038006, 235.1663753159207, 240.05210015849636, 244.6575524506902, 250.13289364633246, 249.74566751022024, 250.1291449183853, 255.86526933622102, 251.08480107136012, 257.37444437042933, 263.51056473232177, 266.1486366156895, 264.7820925624169, 270.7269156396905, 281.1907845623453, 289.72583246388933, 284.4899020879227, 288.93246743245584, 292.9744875766162, 303.10458275192667, 312.0988992452432, 310.1023202125023, 319.4200743329005, 326.80429765535087, 334.90414533198947, 329.9949920748472, 341.2035854816961, 340.0560576487597, 363.0867683845329, 378.4579194618329, 379.0045192967613, 386.10996171296335, 377.5205878901109, 373.61924436497196, 377.4625533038124, 387.29016376127265, 375.6267442198433, 377.2694379166516, 388.2513624705448, 401.3550544431176, 406.16123523809364, 399.28467458648515, 399.8735800142765, 395.73442661053633, 410.63175184094456, 404.25212618581463, 395.999303522399, 405.17713220133743, 400.54920644730123, 377.5057141888378, 374.6032485487132, 367.40244724314, 374.43286525207407, 382.82811243546814, 380.5164752701064, 400.5147228846405, 413.1057955455125, 421.9163536105102, 425.13713732372054, 415.91518736545805, 415.5841966892948, 394.0759004014142, 394.1231773825595, 397.79066869256127, 391.4349347764342, 405.36640392586435, 422.17993919363516, 433.4524133424404, 436.9831752316923, 447.9128541396436, 464.67252464077325, 466.62143317503836, 505.39182718634663, 534.4376803041238, 534.3066617842675, 531.9411538762837, 540.3547616805494, 518.7053376875538, 515.3616205735495, 510.52078869650956, 509.4417348838138, 503.98165752671525, 501.5834276015004, 495.646383802081, 480.15823579275457, 457.416867349314, 450.67604046597927, 445.2797633623103, 445.68663595229265, 446.80411939860625, 457.118043885345, 450.5842585505246, 437.5434813975299, 428.4937639924321, 429.25776277925075, 442.6814869549145, 467.1313237100947, 482.96491629073387, 499.5291062023382, 492.6104083108346, 521.7975202646597, 539.7588670986809, 556.204750797706, 578.3785900715188, 574.8401296669617, 580.9038561898094, 589.6550669355742, 590.377547479427, 618.0471463670997, 619.390363634986, 609.7980972008139, 611.1808071162205, 639.9647348398503, 631.2881997793421, 619.0911912909346, 612.9518711809702, 598.6323209684296, 595.5413292414881, 617.477104977821, 639.9778880239198]

# # for i in range(60*20):
# #     annualized_volatility= calculate_volatility(tuple(points))
# #     # annualized_volatility = (points)
# # elapsed_time = timeit.default_timer() - start_time
# # print(f"Total time: {elapsed_time} seconds")
# # print(annualized_volatility)


# # print("Option cost:")
# # print('European option')

# some_option = Option(european=True,
#                     kind=option_type,
#                     s0=stock_price,
#                     k=strike_price,
#                     t=time_to_expiration,
#                     sigma=volatility,
#                     r=0.05,dv=0)
# from collections import deque
# amounts = deque()

# start_time = timeit.default_timer()
# for i in range(1000):
#     amounts.append(some_option.getPrice(method="MC",iteration=200))

# elapsed_time = timeit.default_timer() - start_time
# print(f"Total time: {elapsed_time} seconds")
# print(sum(amounts)/len(amounts))
# print(min(amounts))
# print(max(amounts))



# def a(b):
#     if b == 50:
#         return b
#     return a(b+1)


# print(a(0))

# def reverse(string):
#     if len(string) == 0:
#         return string
#     print(string)
#     return reverse(string[1:]) + string[0]

# from random import randint

# volatility = 10
# bonustrendranges = [[(-i,i),(randint(1,12000),randint(12001,1_500_000))] for i in range(12)]
# # bonustrendranges = [[((-1,1)),((140_400,421_200))],[((-3,3)),((59400,81000))],[((-8,8)),((8100,21600))],[((-12,12)),((150,3600))]]
# bonustrends = [[randint(*x[0]),randint(*x[1])] for x in bonustrendranges]


# from random import randint

# def addpoint_optimized(lastprice):
#     """returns the new price of the stock"""

#     global bonustrends, bonustrendranges

#     # bonustrends = [[randint(*bonustrendranges[i][0]), randint(*bonustrendranges[i][1])] if trend[1] <= 0 else [trend[0], trend[1] - 1] for i, trend in enumerate(bonustrends)]
#     for i,bonustrend in enumerate(bonustrends):
#         if bonustrend[1] <= 0:#if the time is out
#             bonustrends[i] = [randint(*bonustrendranges[i][0]),randint(*bonustrendranges[i][1])]

#         else:
#             bonustrend[1] -= 1

#     total_trend = sum(trend[0] for trend in bonustrends)
#     total_trend = total_trend if total_trend >= 0 else -1 * (total_trend // 2)
#     highvolitity = volatility + total_trend
#     lowvolitity = -volatility + total_trend
    
#     factor = randint(lowvolitity, highvolitity) / 350_000
#     return lastprice * (1 + factor) if randint(0, 1) else lastprice * (1 - factor)# returns the new price of the stock

# def points100(lastprice,iteration):
#     for _ in range(iteration):
#         lastprice = addpoint_optimized(lastprice)
#     return lastprice
    
# points = [addpoint_optimized(100) for i in range(100000)]

# print("New Run "*5)
# print(sum(points)/len(points))

# print("*"*50)
# points = [points100(100,5_873_400)for i in range(100)]
# print(sum(points)/len(points),'Average')
# print(min(points),'Min')
# print(max(points),'Max')
# print(max(points)-min(points),'Deviation')
# # standard deviation
# import statistics
# std_dev = statistics.stdev(points)
# print("Standard Deviation:", std_dev)
# avrpoints = [point/100 for point in points]
# print(avrpoints)
# print((sum(avrpoints)/len(avrpoints))*100,'Average %')

# with volatility = 5
# 100.0014068216595 Average
# 90.64458480271958 Min
# 110.18290437084235 Max
# 19.538319568122773 Deviation
# Standard Deviation: 1.94196231920995

# with volatility = 25
# 100.10900906938176 Average
# 87.71432861121033 Min
# 110.66061768236355 Max
# 22.946289071153217 Deviation
# Standard Deviation: 2.993402559591465