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

# Read in time steps and velocities
csv_times = np.array(data_cat['time_rel(sec)'].tolist())
csv_data = np.array(data_cat['velocity(m/s)'].tolist())
# Filter from arrival_time_rel onwards 
# csv_times = csv_times[csv_times >= arrival_time_rel]
# csv_data = csv_data[len(csv_data)-len(csv_times):]
# Filter from arrival_time_rel to 60 seconds onwards
# csv_times = csv_times[(csv_times >= arrival_time_rel) & (csv_times <= arrival_time_rel + 60)]

# Filter from time_rel(sec) from 72000 to 76000
time_range_indices = (csv_times >= 72000) & (csv_times <= 76000)
csv_times = csv_times[time_range_indices]
csv_data = csv_data[time_range_indices]

# Remove all values where velocity(m/s) is negative
positive_indices = csv_data > 0
csv_times = csv_times[positive_indices]
csv_data = csv_data[positive_indices]

# print max and min values in csv_data
print(f'Max: {max(csv_data)}')
print(f'Min: {min(csv_data)}')

# Plot the trace!
fig,ax = plt.subplots(1,1,figsize=(10,3))
ax.plot(csv_times,csv_data)
# Make the plot pretty
ax.set_xlim([min(csv_times),max(csv_times)])
ax.set_ylabel('Velocity (m/s)')
ax.set_xlabel('Time (s)')
ax.set_title(f'{test_filename}', fontweight='bold')
# Plot where the arrival time is
arrival_line = ax.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
ax.legend(handles=[arrival_line])

# save the plot
plot_directory = './plots/'
plot_file = f'{plot_directory}{test_filename}.png'
plt.savefig(plot_file)
plt.show()


#13319.829 file 00026
# Notas desde 130.81 a 4186.01 Hz