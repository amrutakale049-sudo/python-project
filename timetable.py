import pandas as pd
import random

# Define data
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
periods = ['Period 1', 'Period 2', 'Period 3', 'Period 4', 'Period 5']
faculty = ['PG ', 'RD ', 'AG ', 'SS ', 'HK ', 'GA ', 'PR ']
# Create an empty DataFrame
timetable = pd.DataFrame(index=days, columns=periods)

# Fill timetable randomly
for day in days:
    selected_faculty = random.sample(faculty, len(periods))  # Ensure no repeat in a day
    for i, period in enumerate(periods):
        timetable.loc[day, period] = selected_faculty[i]

print("Automatic Timetable:")
print(timetable)