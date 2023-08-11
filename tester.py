# import math
# mytuple = (2,3)
# print(math.prod(mytuple))

# def count_words(paragraph):
#   """Counts the number of words in a paragraph."""
#   words = paragraph.split()
#   return len(words)

# print(count_words("Kyronix Solutions Inc. (ticker symbol: KSTON) is a dynamic company specializing in urban mobility solutions. With a visionary team of engineers and transportation experts, Kyronix is at the forefront of revolutionizing urban transportation through innovative technologies like electric vehicles, smart traffic management systems, and autonomous driving solutions. Their commitment to sustainable and efficient mobility drives progress for cities worldwide. "))

import timeit
import statistics
import numpy as np

mylist = [i for i in range(1_000_000)]
myarray = np.array([i for i in range(1_000_000)])
myarray2 = np.array([i for i in range(5)])
myarray2 = np.append(myarray2,2)
print(myarray2)

import numpy as np

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


