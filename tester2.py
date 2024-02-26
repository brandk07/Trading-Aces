
# from datetime import datetime, timedelta

# ytime = datetime(2023, 1, 1, 17, 30, 0)
# mytime2 = datetime(2023, 1, 2, 9, 30, 0)

# difference = mytime2 - ytime
# difference_in_seconds = difference.total_seconds()

# print(difference_in_seconds)
# deltad = timedelta(seconds=difference_in_seconds)
# ytime += deltad
# print(ytime,mytime2)

from datetime import datetime, timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta

# def secsTo930(dt):
#     hour = dt.hour
#     minute = dt.minute
#     hour_diff = (9 - hour) % 24
#     combined_minutes = (hour_diff * 60) + (30 - minute)
#     if combined_minutes > 0:
#         seconds = combined_minutes * 60
#     else:
#         seconds = (combined_minutes + 1440) * 60  # Add 1 day and adjust minutes

#     return seconds

# # Example usage:
# dt = datetime(2023, 1, 1, 17, 30, 0)
# seconds = secsTo930(dt)
# print(f"Time until 9:30 AM on the next day in seconds: {seconds}")
# dt += timedelta(seconds=seconds)
# print(dt)
dt = datetime(2023, 1, 1, 10, 30, 0)
dt2 = datetime(2023, 1, 5, 9, 30, 0)

print((dt - dt.replace(hour=9, minute=30, second=0, microsecond=0)).seconds)

difference = dt2 - dt
# dt1 = datetime(2023, 1, 1, 17, 30, 0)
# dt2 = datetime(2023, 1, 5, 9, 30, 0)

# difference = relativedelta(dt2, dt1)
# difference_in_years = difference.days/365
difference = difference.days/365
print(difference)
print(difference*365)
print(7/(difference))




# start_time = timeit.timeit()
# for i in range(6):
#     mytime += deltadsf

# # Stop the timer
# end_time = timeit.timeit()
# # Calculate and print the elapsed time
# elapsed_time = end_time - start_time
# print("Elapsed time: ", elapsed_time, "seconds")



# import Classes.Gametime as gt

# mytime = gt.GameTime((2023, 7, 4, 9, 40))
# mytime.add_time(1)
# print(mytime)
# print(mytime.isOpen())
# print(mytime.get_time())


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
