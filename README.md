# Solar System Seismonauts 🌔🌌 - NASA Space Apps 2024
Welcome to the **Solar System Seismonauts** repository, a project developed for the **NASA Space Apps Challenge 2024**.
## Challenge

The challenge is to write a computer program to analyze real data from the Apollo missions and the Mars Interior Exploration using Seismic Investigations, Geodesy and Heat Transport (InSight) Lander to identify seismic events! The Example Resources section provides a data packet with continuous seismic records from these missions arranged in training and test subsets, catalogs showing when the known seismic records occur in the training data, and a Python Jupyter Notebook with helpful codes to help you get started. Your team can look at these records to understand the qualities of planetary seismic data, and then try your hand at finding all the seismic events in the test dataset. Maybe you’ll find some additional events not in the current catalogs!

More info [here](https://www.spaceappschallenge.org/nasa-space-apps-2024/challenges/seismic-detection-across-the-solar-system/)

## Project Description 🚀

By studying seismic waves and how fast they travel, we can probe the structure and composition of the Earth and other planets as well, which is crucial for establishing habitability parameters of exoplanets. However, there's just one hiccup: sending data back over long distances in space requires a lot of power. To address this challenge, our team has implemented the following solution:

We used a two-phase ensemble model. First, we applied the STA/LTA algorithm, a state-of-the-art method for seismic detection. We optimized a grid of hyperparameters (windows and triggers) to minimize the mean absolute error (real relative time - predicted relative time) over a training set of 10 files, which outputs different candidate windows for seismic events.

In the (majority) case where the algorithm generated multiple candidate windows for an earthquake, the predicted window was selected as the one with the highest density of anomalies detected by the Isolation Forest algorithm.

This approach resulted in remarkable outcomes on a training set of 50 files, with a mean absolute error of less than five minutes (which corresponds to about 3%) in 40 out of the 50 files.

Sonification is the representation of data sets through sound to facilitate their communication and interpretation. We implemented this concept in the challenge because, not only does it provide a solution to the problem, but it also brings this type of project closer to the public by allowing them to appreciate the data through both music and visualizations, as we have done. This makes the data more accessible. Additionally, sonification is already used in science to assist blind scientists, among other applications. Here's how we implemented it:
With the data received from the final algorithm, we filter the time range where the seismic event occurs.
We fragment the signal into several parts.
We assign a frequency to the velocity (m/s) in each fragment.
We merge all the frequencies into a ```.wav``` file.
We create an animated graph using data from the CSV file (average and median samples).
We add the audio track from step 4 to the video file from step 5.

### Key Features:
- **Seismic data analysis**: We integrate data from public sources, such as NASA missions, to study seismic patterns.
- **Geophysical simulations**: We use simulation tools to model seismic activity in the universe.
- **Interactive visualization**: A multimedia interface allows users to visualize and explore these phenomena.

## Repo structure
```
notebooks - asdfdasf
asdfasdf - asdf
```

## Installation Requirements 📦
To run this project locally, make sure you have the following requirements installed:

- [Python 3.x](https://www.python.org/downloads/)
- [ffmpeg](https://ffmpeg.org)
- Necessary libraries (can be installed using `pip`):

## How to Use
Clone this repository:
```bash
git clone https://github.com/mgarciate/SolarSystemSeismonauts_NASASpaceApps2024.git
```

Open the notebook at:
```bash
cd SolarSystemSeismonauts_NASASpaceApps2024/notebooks
```

Or generate multimedia at:
```bash
cd SolarSystemSeismonauts_NASASpaceApps2024/scripts/display
```

### How to generate multimedia



## Screenshots
![piano frequencies](./resources/images/piano.png?raw=true)

## License
This project is licensed under the terms of the MIT license.