import numpy as np
from scipy.io.wavfile import write

# Mapeamos las notas musicales a frecuencias (escala de Do mayor)
notes = {
    "C": 261.63,
    "D": 293.66,
    "E": 329.63,
    "F": 349.23,
    "G": 392.00,
    "A": 440.00,
    "B": 493.88
}

# Parámetros del terremoto
magnitude = 6.7  # Magnitud del terremoto
depth_km = 13    # Profundidad en km

# Escogemos una nota según la magnitud
if magnitude <= 2:
    note = "C"
elif magnitude <= 3:
    note = "D"
elif magnitude <= 4:
    note = "E"
elif magnitude <= 5:
    note = "F"
else:
    note = "G"

# Frecuencia de la nota seleccionada
frequency = notes[note]

# Duración proporcional a la profundidad
duration_seconds = max(0.5, depth_km / 20) * 5  # Hacemos el sonido más largo

# Generamos la onda de sonido para la nota seleccionada
sample_rate = 44100  # Número de muestras por segundo
t = np.linspace(0, duration_seconds, int(sample_rate * duration_seconds), False)

# Generamos la onda sinusoidal con la frecuencia de la nota seleccionada
tone = np.sin(frequency * 2 * np.pi * t)

# Normalizamos la señal de audio a valores de -32767 a 32767 (int16 para audio PCM)
audio = (tone * 32767).astype(np.int16)

# Guardamos el archivo de audio en formato WAV
wav_file_notes = "./terremoto_sonification_notes.wav"
write(wav_file_notes, sample_rate, audio)

wav_file_notes