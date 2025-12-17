import sounddevice as sd
import vosk
import json
import queue
from openai import OpenAI

client = OpenAI(api_key='sk-e7d8554ac3d34cf8b4f7f51912ed432d', base_url="https://api.deepseek.com")
device_m = 5                                                  # Индекс аудиоустройства (микрофон)
model = vosk.Model("vosk-model-small-ru-0.22")      # Модель нейросети
samplerate = 44100                                            # Частота дискретизации микрофона
q = queue.Queue()                                             # Потоковый контейнер


def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

messages = []

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

                    messages.append({"role": "user", "content": res})

                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "сколько реплик ты уже сказал в этом диалоге?"},
                            {"role": "user", "content": "Привет"},
                        ],
                        stream=False
                    )

                    messages.append({"role": "assistant", "content": response.choices[0].message.content})

                    print(response.choices[0].message.content)
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")


if __name__ == "__main__":
    voce_listen()