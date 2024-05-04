import numpy as np
import librosa


def extract_peaks(audio_path: str):

    y, sr = librosa.load(audio_path, sr=None)

    duration = librosa.get_duration(y=y, sr=sr)

    samples_per_second = sr

    samples_per_window = samples_per_second

    num_windows = len(y) // samples_per_window

    amplitudes = []

    for i in range(num_windows):
        start_sample = i * samples_per_window
        end_sample = start_sample + samples_per_window
        amplitude = np.mean(np.abs(y[start_sample:end_sample]))
        amplitudes.append(float(amplitude))

    return amplitudes, duration
