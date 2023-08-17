from concurrent.futures import ProcessPoolExecutor
import timeit
def square(x):
    return x ** 2

if __name__ == "__main__":

    nums = [i for i in range(1, 10000)]
    num_workers = 1
    start_time = timeit.default_timer()
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        results = executor.map(square, nums)
    # results = map(square, nums)
    print(list(results))  # [1, 4, 9, 16, 25]
    elapsed_time = timeit.default_timer() - start_time
    print(f"Total time: {elapsed_time} seconds")