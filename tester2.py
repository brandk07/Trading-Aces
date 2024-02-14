
import timeit
from datetime import datetime,timedelta

# Start the timer


mytime = datetime(2023, 1, 1, 0, 0)
deltadsf = timedelta(hours=1)
start_time = timeit.timeit()
for i in range(6):
    mytime += deltadsf

# Stop the timer
end_time = timeit.timeit()
# Calculate and print the elapsed time
elapsed_time = end_time - start_time
print("Elapsed time: ", elapsed_time, "seconds")


print(mytime)
print(mytime.weekday())
print(mytime.month)

import Classes.Gametime as gt

mytime = gt.GameTime((2023, 7, 4, 9, 40))
mytime.add_time(1)
print(mytime)
print(mytime.isOpen())
print(mytime.get_time())


# https://docs.python.org/3/library/datetime.html

# # Define the target date and time

# # target_date = datetime(2007, 4, 19, 10, 43)
# target_date = datetime(2023, 10, 27, 11, 15)

# current_date = datetime(2023, 10, 24, 14, 50)
# # Get the current date and time
# current_date = datetime.now()

# # Calculate the time difference
# time_difference = target_date - current_date
# # time_difference = target_date - target_date2

# # Calculate the hours difference
# hours_difference = time_difference.total_seconds() / 3600

# # Print the result
# print(f'You are {(hours_difference):.2f} hours away from October 27, 11:15 AM.')
