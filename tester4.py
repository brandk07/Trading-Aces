from Classes.imports.Latterscroll import LatterScroll
# import pygame
from Defs import point_in_polygon
mypoly = [(150, 150), (277.94524373378374, 228.29440979982337), (300, 300), (300.0, 150.0000000000001), (150, 150)]
print(point_in_polygon((376, 729),mypoly))

# pygame.mixer.init()
# pygame.mixer.music.load("Assets\Sounds\Timo Versemann - Shalom Chaverim.mp3")
# pygame.mixer.music.play()

# while pygame.mixer.music.get_busy():
#     pygame.time.Clock().tick(10)
#     print('playing')
# Suppose we have the following dictionary

# mydict = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
# print(mydict.setdefault('b', 5))
# print(mydict)
# def getAvgReturn(percent,days):
#     neg = 1 if percent > 0 else -1
#     percent = abs(percent)
#     days = 1/(days/365)
#     return ((1+(percent/100)) ** days )* neg

# # avgreturn =  lambda percent,days : ((1+(abs(percent)/100)) ** (1/(days/365)))*100

# print(str(getAvgReturn(-75,1095))+"%")

# print(round(0.004456,2))

# from optionprice import Option as Op
# myOption = Op(european=True,kind="put",s0=9543.754571035066,k=10024.0,t=208,sigma=0.154,r=0.05)
# print(myOption.getPrice(method="BSM",iteration=1))
# print(5%4)
# from datetime import datetime, timedelta
# from Defs import limit_digits
# d1 = datetime.strptime(f"4/19/2035 9:30:00 AM", "%m/%d/%Y %I:%M:%S %p")
# d2 = datetime.strptime(f'12/17/2035 12:58:33 PM', "%m/%d/%Y %I:%M:%S %p")
# print((d2-d1).total_seconds())

# print(limit_digits(13188460.92,12))
import pygame
from Defs import *
import string

# alphabet = [str(i) for i in range(10)]+['.']
# print(alphabet)
# for ii in range(5,180,10):
#     txtlist = [s_render(alphabet[i],ii,(0,0,0)) for i in range(len(alphabet))]
#     print(ii,sum([txt.get_width() for txt in txtlist])/len(txtlist))
# Import necessary libraries
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

# # Example data
# # Independent variables
# currQ = np.array([[1], [2], [3], [4], [5]])
# # Dependent variable
# y = np.array([2, 4, 5, 4, 5])

# # Split the data into training/testing sets
# X_train, X_test, y_train, y_test = train_test_split(currQ, y, test_size=0.2, random_state=0)

# # Create linear regression object
# regr = LinearRegression()

# # Train the model using the training sets
# regr.fit(X_train, y_train)

# # Make predictions using the testing set
# y_pred = regr.predict(X_test)

# # The coefficients
# print('Coefficients: \n', regr.coef_)
# # The mean squared error
# print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))
# # The coefficient of determination: 1 is perfect prediction
# print('Coefficient of determination: %.2f' % regr.score(X_test, y_test))

# finalDict = {str(i)+str(i):(0,0) for i in range(10)}
# testDict = {str(i)+str(i):[] for i in range(10)}
# finalDict['..']= (0,0)
# testDict['..']= []

# INDEPENDENT = [[i] for i in range(5,180,10)]
# for key in testDict:
#     print(key)
#     for i in range(5,180,10):
#         testDict[key].append(s_render(key,i,(0,0,0)).get_width())

#     X_train, X_test, y_train, y_test = train_test_split(INDEPENDENT, testDict[key])

#     regr = LinearRegression()
#     regr.fit(X_train, y_train)
#     y_pred = regr.predict(X_test)
#     print('Coefficients: \n', regr.coef_, key)
#     print(regr.intercept_)
#     finalDict[key] = (round(regr.coef_[0],3),round(regr.intercept_,3))
#     print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))
# print(finalDict)

# from sklearn.ensemble import RandomForestRegressor, 
# from sklearn.metrics import mean_squared_error
# from sklearn.model_selection import train_test_split

# # Assuming the rest of your setup code remains the same

# for key in testDict:

#     X_train, X_test, y_train, y_test = train_test_split(INDEPENDENT, testDict[key])

#     # Use RandomForestRegressor instead of LinearRegression
#     regr = RandomForestRegressor()
#     regr.fit(X_train, y_train)
#     y_pred = regr.predict(X_test)

#     # The rest of your code for printing results and updating finalDict remains the same
#     print('Feature Importance: \n', regr.feature_importances_, key)
#     print('Mean squared error: %.2f' % mean_squared_error(y_test, y_pred))
#     # finalDict[key] = (regr.)

# print(finalDict)
# print(getTSize(5))
# print((233*5+922)/1000)
# from decimal import Decimal, getcontext
# import math
# # Set the precision.
# getcontext().prec = 50

# num1 = Decimal('10.123456789123456789123456789123456789123456789123456789')
# num2 = Decimal('20.123456789123456789123456789123456789123456789123456789')

# result = num1 + num2

# print(result)  # Outputs: 30.246913578246913578246913578246913578246913578246913578
# num = Decimal(str(1106.330826943))*Decimal(str(1.52))
# print(num)

# num *= Decimal(str((10**22)))
# print(format(num, '.5e'))
# print(format(num, '.10f'))

# num = (num/Decimal(str(0.041666666666666664)))
# print(format(num, '.5e'))
# print(format(num, ',.10f'))
from faker import Faker

fake = Faker()

# Generate a random name
print(fake.name())

# Generate a specific number of names
for _ in range(5):
    print(fake.company())

print(fake.ascii_company_email())
print(fake.ascii_email())
print(fake.city())
# print(fake.random_company_product())
print(fake.street_address())
# print(fake.large_company())
print(fake.job())
# print(fake.)

# print([(i%4)+1 for i in range(-3,1)])
print([(i%4)+1 for i in range(1,-3,-1)])
# currQ+1 -> currQ
currQ = 2
# print([(i%4)+1 for i in range(currQ+2,currQ-2,-1)])
print([(i%4)+1 for i in range(currQ-5,currQ-1)])
mylist1,mylist2 = [1,2,3,4,5],[6,7,8,9,10]
for i,ii in zip(mylist1,mylist2):
    print(i,ii)

for i in range(0,1):
    print(i)