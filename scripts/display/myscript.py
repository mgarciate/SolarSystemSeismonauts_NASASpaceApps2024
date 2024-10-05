# Import libraries
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
# Plotting
import matplotlib.pyplot as plt
import os
# Audio
from scipy.io.wavfile import write

# cat_directory = './data/lunar/training/data/S12_GradeA/'
# cat_file = cat_directory + 'xa.s12.00.mhz.1971-02-09HR00_evid00026.csv'
cat_directory = './data/lunar/training/catalogs/'
cat_file = cat_directory + 'apollo12_catalog_GradeA_final.csv'

cat = pd.read_csv(cat_file)
cat

row = cat.iloc[4]
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
notes_max = 8

# Read in time steps and velocities
csv_times = np.array(data_cat['time_rel(sec)'].tolist())
csv_data = np.array(data_cat['velocity(m/s)'].tolist())

# Filter from time_rel(sec) from 72000 to 76000
# file 009
# time_range_indices = (csv_times >= 72000) & (csv_times <= 76000)
# csv_times = csv_times[time_range_indices]
# csv_data = csv_data[time_range_indices]
# file 008
# time_range_indices = (csv_times >= 68000) & (csv_times <= 71000)
# csv_times = csv_times[time_range_indices]
# csv_data = csv_data[time_range_indices]
# file 007
time_range_indices = (csv_times >= 52000) & (csv_times <= 57000)
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

# Audio
# Mapping musical notes to frequencies from 130.81 Hz to 4186.01 Hz
notes_frequencies = {
    "C3": 130.81,
    "D3": 146.83,
    "E3": 164.81,
    "F3": 174.61,
    "G3": 196.00,
    "A3": 220.00,
    "B3": 246.94,
    "C4 (Middle C)": 261.63,
    "D4": 293.66,
    "E4": 329.63,
    "F4": 349.23,
    "G4": 392.00,
    "A4": 440.00,
    "B4": 493.88,
    "C5": 523.25,
    "D5": 587.33,
    "E5": 659.25,
    "F5": 698.46,
    "G5": 783.99,
    "A5": 880.00,
    "B5": 987.77,
    "C6": 1046.50,
    "D6": 1174.66,
    "E6": 1318.51,
    "F6": 1396.91,
    "G6": 1567.98,
    "A6": 1760.00,
    "B6": 1975.53,
    "C7": 2093.00,
    "D7": 2349.32,
    "E7": 2637.02,
    "F7": 2793.83,
    "G7": 3135.96,
    "A7": 3520.00,
    "B7": 3951.07,
    "C8": 4186.01,
}

melody_array = median_values_assigned

# take the first notes_max values from notes_frequencies and save them in a new dictionary
notes_frequencies = {k: notes_frequencies[k] for k in list(notes_frequencies)[:notes_max]}
# take the first notes_max values from notes_frequencies and save them in a new array
notes_frequencies_keys = list(notes_frequencies.keys())

sample_rate = 44100  # Sampling rate in Hz (CD quality)
duration = 0.5  # Duration of each note in seconds
# Fade-in and fade-out duration (in seconds)
fade_duration = 0.01  # 50 ms fade-in and fade-out

# Create a numpy array for the full melody
melody_signal = np.array([])

# Generate the waveform for each note
for note in melody_array:
    frequency = notes_frequencies[notes_frequencies_keys[note]]
    t = np.linspace(0, duration, int(sample_rate * duration), False)  # Time axis for one note
    # Generate a sine wave for the current note
    note_signal = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Apply fade-in and fade-out
    fade_in_len = int(sample_rate * fade_duration)
    fade_out_len = int(sample_rate * fade_duration)
    
    fade_in = np.linspace(0, 1, fade_in_len)
    fade_out = np.linspace(1, 0, fade_out_len)
    
    note_signal[:fade_in_len] *= fade_in
    note_signal[-fade_out_len:] *= fade_out

    # Append the note's signal to the melody
    melody_signal = np.concatenate((melody_signal, note_signal))

# Ensure the waveform is in the correct format (16-bit PCM)
melody_signal = np.int16(melody_signal * 32767)

# Save the generated melody to a WAV file
wav_file = f'{test_filename}.wav'
write(wav_file, sample_rate, melody_signal)

print(f'Melody saved as : {wav_file}')


plot_directory = './plots/'
plot_file = f'{plot_directory}{test_filename}.png'
plt.savefig(plot_file)
plt.show()


#13319.829 file 00026
# Notas desde 130.81 a 4186.01 Hz