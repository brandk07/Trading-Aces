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
# import numpy as np

# myarray = np.array([1, 2, 3, 4, 5, 6, 7, [8, 9, 10]], dtype=object)
# # initialize the array with the correct data type for the second column
# pricepoints = np.array([[3, np.array([1, 2, 3])]], dtype=object)

# # add a new row to the array
# newprice = 1
# gametime = np.array([4, 5, 6])
# value = np.array([newprice, gametime], dtype=object)
# # pricepoints = np.append([myarray, (np.array([newprice, gametime], dtype=object))])
# # pricepoints = np.append(pricepoints, np.array([[1, [4, 5, 6]]], dtype=object))
# # pricepoints = np.append(pricepoints, np.array([[newprice, gametime]], dtype=object))
# pricepoints = np.append(pricepoints, [np.array([newprice, gametime], dtype=object)], axis=0)
# # pricepoints = np.vstack(pricepoints, (np.array([[1, [4, 5, 6]]], dtype=object)))
# # pricepoints = np.vstack(pricepoints, (np.array([[1, [4, 5, 6]]], dtype=object)))


# print(pricepoints)  # output: [[3 [1, 2, 3]], [1, [4, v5, 6]]]

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


# import numpy as np

# my_array = np.array([[1, 2, 3], [4, 5, 6]])

# # Sum the rows (along axis 0)
# row_sums = np.sum(my_array, axis=0)

# # Sum the columns (along axis 1)
# column_sums = np.sum(my_array, axis=1)
# print(row_sums)
# print(column_sums)
# from random import randint
# lst = [[[randint(5,10),[1,2]]] for _ in range(20)]

# print(lst)
# create 9 files using these names in the directory r/Assests/Stockdata/--name--.txt ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO']
directory = r"Assets\Stockdata"
# I want to delete all the files in that directory now so I can create new ones that are .json files
import json
import numpy as np
import timeit
import os
# data = [[100, [0,0,0,0,0,0,0]]]*10
data = []
stocknames = ['SNTOK','KSTON','STKCO','XKSTO','VIXEL','QWIRE','QUBEX','FLYBY','MAGLO','Net Worth']
stockdict = {name:np.array(data,dtype=object) for name in stocknames}

start_time = timeit.default_timer()


for name in stocknames:
    for i in ['recent','hour','day','week','month','year']:
        file_path = f"{directory}/{name}/{i}.json"
        with open(file_path, "w+") as f:
            # f.write("[]")
            json.dump([], f)

elapsed_time = timeit.default_timer() - start_time
print(f"Total time: {elapsed_time} seconds")


# import numpy as np
# import threading
# import timeit
# import os
# import json

# def write_data(name, data, directory):
#     json.dump(data.tolist(), open(os.path.join(directory, f"{name}.json"), "w+"))
#     print(f'Written {name}.json')

# def write_data_parallel(data, stocknames, directory):
#     start_time = timeit.default_timer()
    
#     threads = []
#     for name in stocknames:
#         start_time = timeit.default_timer()
#         thread = threading.Thread(target=write_data, args=(name, data, directory))
#         threads.append(thread)
#         thread.start()
#         elapsed_time = timeit.default_timer() - start_time
#         print(f"{name} time: {elapsed_time} seconds")

#     # Wait for all threads to complete
#     for thread in threads:
#         print(f"Waiting for {thread.name} to complete...")
#         thread.join()
    
#     elapsed_time = timeit.default_timer() - start_time
#     print(f"Total time: {elapsed_time} seconds")

# if __name__ == "__main__":
#     data = np.random.randint(0, 100, size=(100000, 2))
#     stocknames = ['SNTOK', 'KSTON', 'STKCO', 'XKSTO', 'VIXEL', 'QWIRE', 'QUBEX', 'FLYBY', 'MAGLO', 'Net Worth']
#     directory = "Assets/Stockdata"  # Relative path without leading slash
    
#     write_data_parallel(data, stocknames, directory)





# import os
# import dask.dataframe as dd

# # List of stocknames
# stocknames = ['SNTOK', 'KSTON', 'STKCO', 'XKSTO', 'VIXEL', 'QWIRE', 'QUBEX', 'FLYBY', 'MAGLO', 'Net Worth']
# directory = os.path.join("Assets", "Stockdata")

# # Create a list of file paths
# file_paths = [os.path.join(directory, f"{name}.parquet") for name in stocknames]

# # Read Parquet files into Dask DataFrames
# dataframes = [dd.read_parquet(file_path) for file_path in file_paths]


# # Now you have a list of Dask DataFrames, one for each stockname
# # You can work with these DataFrames for further analysis
