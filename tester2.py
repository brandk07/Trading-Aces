from datetime import datetime

# Define the target date and time

target_date = datetime(2007, 4, 19, 10, 43)
target_date = datetime(2023, 10, 27, 11, 15)

current_date = datetime(2023, 10, 24, 14, 50)
# Get the current date and time
current_date = datetime.now()

# Calculate the time difference
time_difference = target_date - current_date
# time_difference = target_date - target_date2

# Calculate the hours difference
hours_difference = time_difference.total_seconds() / 3600

# Print the result
print(f'You are {hours_difference:.2f} hours away from October 27, 11:15 AM.')
