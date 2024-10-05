# 13319.829 file 00026
# Musical frequencies from 130.81 to 4186.01 Hz

import json
import numpy as np
import pandas as pd
from obspy import read
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import os
from scipy.io.wavfile import write

# Load the notes_frequencies from the JSON file
def load_notes_frequencies(json_file):
    with open(json_file, 'r') as f:
        notes_frequencies = json.load(f)
    return notes_frequencies

# Load data from the catalog and data files
def load_catalog_and_data(cat_directory, cat_file, row_index, data_directory):
    # Load catalog CSV
    cat = pd.read_csv(cat_directory + cat_file)
    row = cat.iloc[row_index]
    
    # Extract arrival time and filename
    arrival_time = datetime.strptime(row['time_abs(%Y-%m-%dT%H:%M:%S.%f)'],'%Y-%m-%dT%H:%M:%S.%f')
    arrival_time_rel = row['time_rel(sec)']
    test_filename = row.filename
    
    # Load data from the corresponding file
    csv_file = f'{data_directory}{test_filename}.csv'
    data_cat = pd.read_csv(csv_file)
    
    return data_cat, test_filename, arrival_time, arrival_time_rel

# Process the data by filtering and normalizing values
def process_data(data_cat, time_range, num_parts):
    # Convert to numpy arrays
    csv_times = np.array(data_cat['time_rel(sec)'].tolist())
    csv_data = np.array(data_cat['velocity(m/s)'].tolist())
    
    # Filter the data within the specified time range
    time_range_indices = (csv_times >= time_range[0]) & (csv_times <= time_range[1])
    csv_times = csv_times[time_range_indices]
    csv_data = csv_data[time_range_indices]
    
    # Remove negative values
    positive_indices = csv_data > 0
    csv_times = csv_times[positive_indices]
    csv_data = csv_data[positive_indices]
    
    # Normalize data and calculate the intervals
    max_value = np.max(csv_data)
    min_value = np.min(csv_data)
    time_intervals = np.linspace(min(csv_times), max(csv_times), num_parts + 1)
    
    return csv_times, csv_data, time_intervals, max_value, min_value

# Calculate mean and median values for each interval and assign values between 0 and value_range
def calculate_mean_median_values(csv_times, csv_data, time_intervals, num_parts, value_range):
    # Initialize lists to store mean and median values for each interval
    mean_values = []
    median_values = []
    
    for i in range(num_parts):
        # Filter the data for the current interval
        part_indices = (csv_times >= time_intervals[i]) & (csv_times < time_intervals[i + 1])
        part_data = csv_data[part_indices]
        
        if len(part_data) > 0:
            mean_value = np.mean(part_data)
            median_value = np.median(part_data)
            
            mean_values.append(mean_value)
            median_values.append(median_value)

    # Calculate min and max for mean and median values
    min_mean_value = min(mean_values)
    max_mean_value = max(mean_values)
    min_median_value = min(median_values)
    max_median_value = max(median_values)

    # Normalize and assign values between 1 and value_range based on mean and median values
    mean_values_assigned = [(int(((mean_value - min_mean_value) / (max_mean_value - min_mean_value)) * (value_range - 1)))
                            for mean_value in mean_values]

    median_values_assigned = [(int(((median_value - min_median_value) / (max_median_value - min_median_value)) * (value_range - 1)))
                              for median_value in median_values]
    
    return mean_values_assigned, median_values_assigned

# Plot the processed data with annotations
def plot_data(csv_times, csv_data, time_intervals, arrival_time_rel, test_filename):
    fig, ax = plt.subplots(1, 1, figsize=(10, 3))
    ax.plot(csv_times, csv_data)
    ax.set_xlim([min(csv_times), max(csv_times)])
    ax.set_ylabel('Velocity (m/s)')
    ax.set_xlabel('Time (s)')
    ax.set_title(f'{test_filename}', fontweight='bold')

    for i in range(len(time_intervals) - 1):
        midpoint = (time_intervals[i] + time_intervals[i + 1]) / 2
        ax.axvline(x=midpoint, color='red', linestyle='--', alpha=0.7)
        
        part_indices = (csv_times >= time_intervals[i]) & (csv_times < time_intervals[i + 1])
        part_data = csv_data[part_indices]
        
        if len(part_data) > 0:
            mean_value = np.mean(part_data)
            ax.text(midpoint, mean_value, f'{mean_value:.2e}', color='blue', fontsize=10, ha='center')
            # Alternating background color
            color = 'lightgreen' if i % 2 == 0 else 'lightblue'
            ax.axvspan(time_intervals[i], time_intervals[i + 1], facecolor=color, alpha=0.6)
    
    # Plot the arrival time
    ax.axvline(x=arrival_time_rel, c='red', label='Rel. Arrival')
    ax.legend()
    
    plot_directory = './plots/'
    plot_file = f'{plot_directory}{test_filename}.png'
    plt.savefig(plot_file)
    plt.show()

    print(f"Plot saved as: {plot_file}")

# Generate audio melody based on assigned notes
def generate_melody(melody_array, sample_rate, duration, fade_duration, notes_frequencies, notes_frequencies_keys, test_filename):
    melody_signal = np.array([])
    print(f"Melody array: {melody_array}")
    for note in melody_array:
        frequency = notes_frequencies[notes_frequencies_keys[note]]
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        note_signal = 0.5 * np.sin(2 * np.pi * frequency * t)

        fade_in_len = int(sample_rate * fade_duration)
        fade_out_len = int(sample_rate * fade_duration)
        fade_in = np.linspace(0, 1, fade_in_len)
        fade_out = np.linspace(1, 0, fade_out_len)
        
        note_signal[:fade_in_len] *= fade_in
        note_signal[-fade_out_len:] *= fade_out

        melody_signal = np.concatenate((melody_signal, note_signal))
    
    melody_signal = np.int16(melody_signal * 32767)
    wav_file = f'{test_filename}.wav'
    write(wav_file, sample_rate, melody_signal)
    print(f"Melody saved as: {wav_file}")

# Main function to call the above tasks
def main():
    # Parameters
    cat_directory = './data/lunar/training/catalogs/'
    cat_file = 'apollo12_catalog_GradeA_final.csv'
    data_directory = './data/lunar/training/data/S12_GradeA/'
    row_index = 6
    time_range = (72000, 76000)
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
# time_range_indices = (csv_times >= 52000) & (csv_times <= 57000)
# csv_times = csv_times[time_range_indices]
# csv_data = csv_data[time_range_indices]

    num_parts = 20
    value_range = 8

    # Load data
    data_cat, test_filename, arrival_time, arrival_time_rel = load_catalog_and_data(
        cat_directory, cat_file, row_index, data_directory
    )

    # Process data
    csv_times, csv_data, time_intervals, max_value, min_value = process_data(data_cat, time_range, num_parts)
    print(f"Max value: {max_value}")
    print(f"Min value: {min_value}")

    # Calculate mean and median values and assign values between 1 and value_range
    mean_values_assigned, median_values_assigned = calculate_mean_median_values(csv_times, csv_data, time_intervals, num_parts, value_range)
    print(f"Mean assigned value: {mean_values_assigned}")
    print(f"Median assigned value: {median_values_assigned}")

    # Load notes frequencies from JSON file
    json_file = 'notes_frequencies.json'
    notes_frequencies = load_notes_frequencies(json_file)
    
    notes_frequencies_trimmed = {k: notes_frequencies[k] for k in list(notes_frequencies)[:value_range]}
    notes_frequencies_keys = list(notes_frequencies_trimmed.keys())
    
    melody_array = mean_values_assigned
    
    # Generate melody
    sample_rate = 44100  # CD quality
    duration = 0.5  # 0.5 seconds per note
    fade_duration = 0.01  # Fade in/out duration (10 ms)
    
    generate_melody(melody_array, sample_rate, duration, fade_duration, notes_frequencies_trimmed, notes_frequencies_keys, test_filename)
    
    # Plot data
    plot_data(csv_times, csv_data, time_intervals, arrival_time_rel, test_filename)

# Run the main function
if __name__ == "__main__":
    main()
