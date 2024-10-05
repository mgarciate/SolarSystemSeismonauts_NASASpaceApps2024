# Import libraries
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
# cat_directory = './data/lunar/training/data/S12_GradeA/'
# cat_file = cat_directory + 'xa.s12.00.mhz.1971-02-09HR00_evid00026.csv'
cat_directory = './data/lunar/training/catalogs/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'

cat = pd.read_csv(cat_file)
cat

row = cat.iloc[6]
arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
arrival_time

# If we want the value of relative time, we don't need to use datetime
arrival_time_rel = row['time_rel(sec)']
arrival_time_rel
print(arrival_time_rel)

# Let's also get the name of the file
test_filename = row.filename
test_filename

print(test_filename)

data_directory = './data/lunar/training/data/S12_GradeA/'
csv_file = f'{data_directory}{test_filename}.csv'
data_cat = pd.read_csv(csv_file)
data_cat

# Set the number of parts
num_parts = 20
# Set the range for the assigned values (1 to value_range)
value_range = 30

# Read in time steps and velocities
csv_times = np.array(data_cat['time_rel(sec)'].tolist())
csv_data = np.array(data_cat['velocity(m/s)'].tolist())

# Filter from time_rel(sec) from 72000 to 76000
time_range_indices = (csv_times >= 72000) & (csv_times <= 76000)
csv_times = csv_times[time_range_indices]
csv_data = csv_data[time_range_indices]

# Remove all values where velocity(m/s) is negative
positive_indices = csv_data > 0
csv_times = csv_times[positive_indices]
csv_data = csv_data[positive_indices]

# Time intervals for dividing the plot
time_min, time_max = min(csv_times), max(csv_times)
time_intervals = np.linspace(time_min, time_max, num_parts + 1)

max_value = np.max(csv_data)
min_value = np.min(csv_data)
print(f'Max: {max_value}')
print(f'Min: {min_value}')

# Plot the trace!
fig,ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(csv_times,csv_data)
# Make the plot pretty
ax.set_xlim([min(csv_times),max(csv_times)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')
ax.set_title(f'{test_filename}', fontweight='bold')

# Process each part, calculate mean/median, and set background color
median_values_assigned = []
mean_values_assigned = []

for i in range(num_parts):
    midpoint = (time_intervals[i] + time_intervals[i + 1]) / 2
    ax.axvline(x=midpoint, color='red', linestyle='--', alpha=0.7)
    
    # Filter the data for the current interval
    part_indices = (csv_times >= time_intervals[i]) & (csv_times < time_intervals[i + 1])
    part_data = csv_data[part_indices]
    
    if len(part_data) > 0:
        mean_value = np.mean(part_data)
        median_value = np.median(part_data)

        # Light background color to each part
        if i % 2 == 0:
            ax.axvspan(time_intervals[i], time_intervals[i + 1], facecolor='lightgreen', alpha=0.6)
        else:
            ax.axvspan(time_intervals[i], time_intervals[i + 1], facecolor='lightblue', alpha=0.6)
        
        # Show the mean above the interval
        ax.text(midpoint, mean_value, f'{mean_value:.2e}', color='blue', fontsize=10, ha='center')

        # Assign a value between 1 and value_range based on the median
        normalized_median = (median_value - min_value) / (max_value - min_value)
        median_assigned_value = int(normalized_median * (value_range - 1)) + 1
        median_values_assigned.append(median_assigned_value)
        
        # Assign a value between 1 and value_range based on the mean
        normalized_mean = (mean_value - min_value) / (max_value - min_value)
        mean_assigned_value = int(normalized_mean * (value_range - 1)) + 1
        mean_values_assigned.append(mean_assigned_value)

# Print the maximum, minimum values, and the array with the assigned values
print(f'Max value: {max_value}')
print(f'Min value: {min_value}')
print(f'Assigned values to median: {median_values_assigned}')
print(f'Assigned values to mean: {mean_values_assigned}')

# Plot where the arrival time is
arrival_line = ax.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
ax.legend(handles=[arrival_line])

plot_directory = './plots/'
plot_file = f'{plot_directory}{test_filename}.png'
plt.savefig(plot_file)
plt.show()


#13319.829 file 00026
# Notas desde 130.81 a 4186.01 Hz