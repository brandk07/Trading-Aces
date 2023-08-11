# import math
# mytuple = (2,3)
# print(math.prod(mytuple))

# def count_words(paragraph):
#   """Counts the number of words in a paragraph."""
#   words = paragraph.split()
#   return len(words)

# print(count_words("Kyronix Solutions Inc. (ticker symbol: KSTON) is a dynamic company specializing in urban mobility solutions. With a visionary team of engineers and transportation experts, Kyronix is at the forefront of revolutionizing urban transportation through innovative technologies like electric vehicles, smart traffic management systems, and autonomous driving solutions. Their commitment to sustainable and efficient mobility drives progress for cities worldwide. "))

# import timeit
# import statistics
# import numpy as np

# mylist = [i for i in range(1_000_000)]
# myarray = np.array([i for i in range(1_000_000)])
# myarray2 = np.array([i for i in range(5)])
# myarray2 = np.append(myarray2,2)
# print(myarray2)

# import numpy as np
import numpy as np

myarray = np.array([1, 2, 3, 4, 5, 6, 7, [8, 9, 10]], dtype=object)
# initialize the array with the correct data type for the second column
pricepoints = np.array([[3, np.array([1, 2, 3])]], dtype=object)

# add a new row to the array
newprice = 1
gametime = np.array([4, 5, 6])
value = np.array([newprice, gametime], dtype=object)
# pricepoints = np.append([myarray, (np.array([newprice, gametime], dtype=object))])
# pricepoints = np.append(pricepoints, np.array([[1, [4, 5, 6]]], dtype=object))
# pricepoints = np.append(pricepoints, np.array([[newprice, gametime]], dtype=object))
pricepoints = np.append(pricepoints, [np.array([newprice, gametime], dtype=object)], axis=0)
# pricepoints = np.vstack(pricepoints, (np.array([[1, [4, 5, 6]]], dtype=object)))
# pricepoints = np.vstack(pricepoints, (np.array([[1, [4, 5, 6]]], dtype=object)))


print(pricepoints)  # output: [[3 [1, 2, 3]], [1, [4, v5, 6]]]

# medianpoint = np.median(mylist)
# newlist = mylist[-50000:]
# start_time = timeit.default_timer()
# newarray = mylist[-50000:]
# end_time = timeit.default_timer()
# print("Elapsed time:", end_time - start_time, "seconds")

# start_time = timeit.default_timer()
# newarray = myarray[-50000:]
# end_time = timeit.default_timer()
# print("Elapsed time:", end_time - start_time, "seconds")
# # print(medianpoint)

# import time
# import numpy as np

# start_time = time.time()
# mylist = np.arange(0, 1000000, 1000)
# print(len(mylist))
# end_time = time.time()

# print("Elapsed time:", end_time - start_time, "seconds")


