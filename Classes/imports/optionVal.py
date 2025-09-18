import numpy as np

class OptionVal:
    """
    function: initialize an option
    :parm european: True if the option is an European option and False if it's an American one
    :parm kind: 1 for call option while -1 for put option. Other number are not valid
    :parm s0: initial price
    :parm k: strike price
    :parm sigma: volatility of stock
    :parm r: risk free interest rate per annu
    :[optional]parm dv: dividend rate. 0 for non-stock option, which is also the default
    :[optional]parm start: beginning date of the option, string like '2008-02-14',default today
    :[optional]parm end: end date of the option, string like '2008-02-14',default today plus param t
    :[optional]param t: time of the option in days
    :Note that if start,end and t are all given, then t will choose the difference between end and start
    :Note that either t or (start and end) should exists
    :return Option
    """
    def __init__(self, european, kind, s0, k, r, sigma, dv=0, t=None, start=None, end=None):
        if t is None and (start is None or end is None):
            raise TypeError("Either t or (start and end) must be given.")
        if kind.lower() not in ["call","put"]:
            raise TypeError("kind should be either put or call.")
        if not isinstance(european,bool):
            raise TypeError("european should be either True or False")
        if not isinstance(s0,(int, float)):
            raise TypeError("s0 should be a number")
        if not isinstance(k,(int, float)):
            raise TypeError("k should be a number")
        if not isinstance(r,(int, float)):
            raise TypeError("r should be a number")
        if not isinstance(sigma,(int, float)):
            raise TypeError("sigma should be a number")
        if not isinstance(dv,(int, float)):
            raise TypeError("dv should be a number")
        self.european = european
        self.kind = 1 if kind.lower() == 'call' else -1
        self.s0 = s0# 1 share price
        self.k = k# strike price
        self.sigma = sigma
        self.r = r# risk free rate
        self.dv = dv# dividend rate
        self.t = t/365# time in years, if t is given, then it will be used as the time span of the option

    def setValues(self, underPrice=None, interestRate=None, volatility=None, strike=None, optionType=None, dividend=None, days=None, dv=None):
        if underPrice: self.s0 = underPrice
        if interestRate: self.r = interestRate
        if volatility: self.sigma = volatility
        if dividend: self.dv = dividend
        if days: self.t = days
        if strike: self.k = strike
        if optionType: self.kind = 1 if optionType.lower() == 'call' else -1
        if self.k == 0: self.k = 1
        if dv: self.dv = dv

    def _norm_cdf(self, x):
        """
        Highly accurate normal cumulative distribution function using numpy
        Uses Hart's algorithm for very high precision
        """
        x = np.asarray(x)
        
        # For very large negative values, return 0
        # For very large positive values, return 1
        result = np.zeros_like(x, dtype=np.float64)
        
        # Handle extreme cases
        extreme_neg = x < -8.0
        extreme_pos = x > 8.0
        normal_range = (~extreme_neg) & (~extreme_pos)
        
        result[extreme_neg] = 0.0
        result[extreme_pos] = 1.0
        
        # For normal range, use high precision approximation
        if np.any(normal_range):
            x_norm = x[normal_range]
            
            # Use a more accurate polynomial approximation
            # Based on Hart et al. Computer Approximations (1968)
            t = 1.0 / (1.0 + 0.2316419 * np.abs(x_norm))
            
            # Polynomial coefficients for higher accuracy
            b1 =  0.319381530
            b2 = -0.356563782
            b3 =  1.781477937
            b4 = -1.821255978
            b5 =  1.330274429
            
            # Calculate the polynomial
            poly = t * (b1 + t * (b2 + t * (b3 + t * (b4 + t * b5))))
            
            # Calculate the CDF
            pdf = np.exp(-0.5 * x_norm * x_norm) / np.sqrt(2.0 * np.pi)
            cdf_val = 1.0 - pdf * poly
            
            # Handle negative values using symmetry
            neg_mask = x_norm < 0
            cdf_val[neg_mask] = 1.0 - cdf_val[neg_mask]
            
            result[normal_range] = cdf_val
        
        return result

    def getPrice(self, method="BSM", iteration=5000):
        # print(f"days left: {self.t*365}, initial price: {self.s0}, strike price: {self.k}, volatility: {self.sigma}, risk free rate: {self.r}, dividend rate: {self.dv}, type {'put' if self.kind == -1 else 'call'}")
        
        if method == "BSM" or method.upper() == "B-S-M":
            if self.european or self.kind == 1:
                d_1 = (np.log(self.s0 / self.k) + (
                        self.r - self.dv + .5 * self.sigma ** 2) * self.t) / self.sigma / np.sqrt(
                    self.t)
                d_2 = d_1 - self.sigma * np.sqrt(self.t)
                
                result = self.kind * self.s0 * np.exp(-self.dv * self.t) * self._norm_cdf(
                    self.kind * d_1) - self.kind * self.k * np.exp(-self.r * self.t) * self._norm_cdf(self.kind * d_2)
                
                # print(f"final price calculation: {result}")
                return result

        elif method.upper() == "MC" or method.upper() == "Monte Carlo":
            if self.european or self.kind == 1:
                zt = np.random.normal(0, 1, iteration)
                st = self.s0 * np.exp((self.r - self.dv - .5 * self.sigma ** 2) * self.t + self.sigma * self.t ** .5 * zt)
                st = np.maximum(self.kind * (st - self.k), 0)
                return np.average(st) * np.exp(-self.r * self.t)

        elif method.upper() == "BT" or method.upper() == "Binomial Tree":
            delta = self.t / iteration
            u = np.exp(self.sigma * np.sqrt(delta))
            d = 1 / u
            p = (np.exp((self.r - self.dv) * delta) - d) / (u - d)
            
            tree = np.arange(0,iteration * 2 + 2,2,dtype=np.float64)
            tree[iteration//2 + 1:] = tree[:(iteration+1)//2][::-1]
            np.multiply(tree,-1,out=tree)
            np.add(tree,iteration,out=tree)
            np.power(u,tree[:iteration//2],out=tree[:iteration//2])
            np.power(d,tree[iteration//2:],out=tree[iteration//2:])
            np.maximum((self.s0 * tree - self.k) * self.kind,0,out=tree)

            for j in range(iteration):
                newtree = tree[:-1] * p + tree[1:] * (1 - p)
                newtree = newtree * np.exp(-self.r * delta)
                if not self.european:
                    compare = np.abs(iteration - j - 1 - np.arange(tree.size - 1) * 2).astype(np.float64)
                    np.power(u,compare[:len(compare)//2],out=compare[:len(compare)//2])
                    np.power(d,compare[len(compare)//2:],out=compare[len(compare)//2:])
                    np.multiply(self.s0,compare,out=compare)
                    np.subtract(compare,self.k,out=compare)
                    np.multiply(compare,self.kind,out=compare)
                    np.maximum(newtree, compare,out=newtree)
                tree = newtree

            return tree[0]

    def __repr__(self):
        info = "{:<16}{}".format("Type:","European" if self.european else "American")
        info += "\n{:<16}{}".format("Kind:","call" if self.kind == 1 else "put")
        info += "\n{:<16}{}".format("Price initial:",self.s0)
        info += "\n{:<16}{}".format("Price strike:",self.k)
        info += "\n{:<16}{}".format("Volatility:",str(self.sigma*100)+"%")
        info += "\n{:<16}{}".format("Risk free rate:",str(self.r*100)+"%")
        if self.dv != 0:
            info += "\n{:<16}{}".format("Dividend rate:",str(self.dv*100)+"%")
        info += "\n{:<16}{}".format("Time span:",str(int(self.t * 365)) + " days")
        return info

    def __str__(self):
        return self.__repr__()

# if __name__=='__main__':
#     a = OptionVal(european=True,
#                 kind='put',
#                 s0=120,
#                 k=120,
#                 t=.3,
#                 sigma=0.2,
#                 r=0.05,
#                 dv=0)
#     print(a)
#     print(a.getPrice())
#     # print(a.getPrice(method='MC',iteration = 500000))
#     # print(a.getPrice(method='BT',iteration = 1000))
# import scipy.stats as sps
# import numpy as np
# import timeit

# class OptionVal2:

#     """
#     function: initialize an option
#     :parm european: True if the option is an European option and False if it's an American one
#     :parm kind: 1 for call option while -1 for put option. Other number are not valid
#     :parm s0: initial price
#     :parm k: strike price
#     :parm sigma: volatility of stock
#     :parm r: risk free interest rate per annu
#     :[optional]parm dv: dividend rate. 0 for non-stock option, which is also the default
#     :[optional]parm start: beginning date of the option, string like '2008-02-14',default today
#     :[optional]parm end: end date of the option, string like '2008-02-14',default today plus param t
#     :[optional]param t: time of the option in days
#     :Note that if start,end and t are all given, then t will choose the difference between end and start
#     :Note that either t or (start and end) should exists
#     :return Option
#     """
#     def __init__(self, european, kind, s0, k, r, sigma, dv=0, t=None, start=None, end=None):
#         if t is None and (start is None or end is None):
#             raise TypeError("Either t or (start and end) must be given.")
#         if kind.lower() not in ["call","put"]:
#             raise TypeError("kind should be either put or call.")
#         if not isinstance(european,bool):
#             raise TypeError("european should be either True or False")
#         if not isinstance(s0,(int, float)):
#             raise TypeError("s0 should be either True or False")
#         if not isinstance(k,(int, float)):
#             raise TypeError("k should be either True or False")
#         if not isinstance(r,(int, float)):
#             raise TypeError("r should be either True or False")
#         if not isinstance(sigma,(int, float)):
#             raise TypeError("sigma should be either True or False")
#         if not isinstance(dv,(int, float)):
#             raise TypeError("dv should be either True or False")
#         self.european = european
#         self.kind = 1 if kind.lower() == 'call' else -1
#         self.s0 = s0# 1 share price
#         self.k = k# strike price
#         self.sigma = sigma
#         self.r = r# risk free rate
#         self.dv = dv# dividend rate
#         # self.start = np.datetime64(start,'D') if start else np.datetime64('today', 'D') 
#         # self.end = np.datetime64(end,'D') if end else np.datetime64('today', 'D') + np.timedelta64(t,'D')
#         self.t = t/365

#     """
#     function: calculate the option price
#     :parm method: indicate which method should be used to calculate.It can be one of "BSM","BT" and "MC".
#     :parm iteration: the iteration times for "BT" and "MC"
#     :return price
#     """
#     def setValues(self, underPrice=None, interestRate=None, volatility=None, strike=None, optionType=None, dividend=None, days=None, dv=None):
#         if underPrice: self.s0 = underPrice
#         if interestRate: self.r = interestRate
#         if volatility: self.sigma = volatility
#         if dividend: self.dv = dividend
#         if days: self.t = days
#         if strike: self.k = strike
#         if optionType: self.kind = 1 if optionType.lower() == 'call' else -1
#         if self.k == 0: self.k = 1
#         if dv: self.dv = dv


#     def getPrice(self,method="BSM",iteration = 5000):
#         if method == "BSM" or method.upper() == "B-S-M":
#             if self.european or self.kind == 1:
#                 d_1 = (np.log(self.s0 / self.k) + (
#                         self.r - self.dv + .5 * self.sigma ** 2) * self.t) / self.sigma / np.sqrt(
#                     self.t)
#                 d_2 = d_1 - self.sigma * np.sqrt(self.t)
#                 return self.kind * self.s0 * np.exp(-self.dv * self.t) * sps.norm.cdf(
#                     self.kind * d_1) - self.kind * self.k * np.exp(-self.r * self.t) * sps.norm.cdf(self.kind * d_2)


#         elif method.upper() == "MC" or method.upper() == "Monte Carlo":
#             if self.european or self.kind == 1:
#                 zt = np.random.normal(0, 1, iteration)
#                 st = self.s0 * np.exp((self.r - self.dv - .5 * self.sigma ** 2) * self.t + self.sigma * self.t ** .5 * zt)
#                 st = np.maximum(self.kind * (st - self.k), 0)
#                 return np.average(st) * np.exp(-self.r * self.t)


#         elif method.upper() == "BT" or method.upper() == "Binomial Tree":
#             delta = self.t / iteration
#             u = np.exp(self.sigma * np.sqrt(delta))
#             d = 1 / u
#             p = (np.exp((self.r - self.dv) * delta) - d) / (u - d)
            
#             tree = np.arange(0,iteration * 2 + 2,2,dtype=np.float)
#             tree[iteration//2 + 1:] = tree[:(iteration+1)//2][::-1]
#             np.multiply(tree,-1,out=tree)
#             np.add(tree,iteration,out=tree)
#             np.power(u,tree[:iteration//2],out=tree[:iteration//2])
#             np.power(d,tree[iteration//2:],out=tree[iteration//2:])
#             np.maximum((self.s0 * tree - self.k) * self.kind,0,out=tree)

#             for j in range(iteration):
#                 newtree = tree[:-1] * p + tree[1:] * (1 - p)
#                 newtree = newtree * np.exp(-self.r * delta)
#                 if not self.european:
#                     compare = np.abs(iteration - j - 1 - np.arange(tree.size - 1) * 2).astype(np.float)
#                     np.power(u,compare[:len(compare)//2],out=compare[:len(compare)//2])
#                     np.power(d,compare[len(compare)//2:],out=compare[len(compare)//2:])
#                     np.multiply(self.s0,compare,out=compare)
#                     np.subtract(compare,self.k,out=compare)
#                     np.multiply(compare,self.kind,out=compare)
#                     np.maximum(newtree, compare,out=newtree)
#                 tree = newtree

#             return tree[0]

#     def __repr__(self):
#         info = "{:<16}{}".format("Type:","European" if self.european else "American")
#         info += "\n{:<16}{}".format("Kind:","call" if self.kind == 1 else "put")
#         info += "\n{:<16}{}".format("Price initial:",self.s0)
#         info += "\n{:<16}{}".format("Price strike:",self.k)
#         info += "\n{:<16}{}".format("Volatility:",str(self.sigma*100)+"%")
#         info += "\n{:<16}{}".format("Risk free rate:",str(self.r*100)+"%")
#         if self.dv != 0:
#             info += "\n{:<16}{}".format("Dividend rate:",str(self.dv*100)+"%")
#         # info += "\n{:<16}{}".format("Start Date:",self.start)
#         # info += "\n{:<16}{}".format("Expire Date:",self.end)
#         info += "\n{:<16}{}".format("Time span:",str(int(self.t * 365)) + " days")
#         return info

#     def __str__(self):
#         return self.__repr__()

# if __name__=='__main__':
#     a = OptionVal(european=True,
#                 kind='call',
#                 s0=38163.4905/100,
#                 k=45000/100,
#                 t=100000.9,
#                 sigma=0.3643,
#                 r=0.05,
#                 dv=0.0089)
#     print(a)
#     print(a.getPrice()*100)
#     b = OptionVal2(european=True,
#                 kind='call',
#                 s0=38163.4905/100,
#                 k=45000/100,
#                 t=100000.9,
#                 sigma=0.3643,
#                 r=0.05,
#                 dv=0.0089)
#     print(b)
#     print(b.getPrice()*100)
#     # print(a.getPrice(method='MC',iteration = 500000))
#     # print(a.getPrice(method='BT',iteration = 1000))