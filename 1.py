import sounddevice as sd
import vosk
import json
import queue

device_m = 2                                                  # Индекс аудиоустройства (микрофон)
model = vosk.Model("model_stt/vosk-model-small-ru-0.22")      # Модель нейросети
samplerate = 44100                                            # Частота дискретизации микрофона
q = queue.Queue()                                             # Потоковый контейнер


def q_callback(indata, frames, time, status):
    q.put(bytes(indata))


def voce_listen():
    with sd.RawInputStream(callback=q_callback, channels=1, samplerate=samplerate, device=device_m, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)
        sd.sleep(-20)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Фраза целиком: {res}")
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")


if __name__ == "__main__":
    voce_listen()