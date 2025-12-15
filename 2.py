import sounddevice as sd
import numpy as np

# Параметры записи
fs = 44100  # Частота дискретизации
duration = 5  # Длительность записи в секундах
channels = 1  # Количество каналов (1 для моно)

print("Начинаем запись...")
# Запись звука с микрофона
recording = sd.rec(int(fs * duration), samplerate=fs, channels=channels, dtype='float32')
sd.wait()  # Ожидаем завершения записи
print("Запись завершена.")

print("Воспроизведение записанного звука...")
# Воспроизведение записанного звука через динамик
sd.play(recording, fs)
sd.wait()
print("Воспроизведение завершено.")