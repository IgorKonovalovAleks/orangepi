import sounddevice as sd
import vosk
import json
import queue
import os
from openai import OpenAI

device_m = 5                                                  # Индекс аудиоустройства (микрофон)
model = vosk.Model(r"model_stt/vosk-model-small-ru-0.22/vosk-model-small-ru-0.22")      # Модель нейросети
samplerate = 44100                                            # Частота дискретизации микрофона
q = queue.Queue()                                             # Потоковый контейнер
print(sd.query_devices())

def q_callback(indata, frames, time, status):
    q.put(bytes(indata))

messages = []
client = OpenAI(api_key='sk-e7d8554ac3d34cf8b4f7f51912ed432d', base_url="https://api.deepseek.com")

def voce_listen():
    with sd.RawInputStream(callback=q_callback, channels=2, samplerate=samplerate, device=device_m, dtype='int16'):
        rec = vosk.KaldiRecognizer(model, samplerate)
        sd.sleep(-20)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())["text"]
                if res:
                    print(f"Фраза целиком: {res}")
                    messages.append(res)

                    response = client.chat.completions.create(
                        model="deepseek-chat",
                        messages=[
                            {"role": "system", "content": "Тебя зовут Густав и ты художник. Твоё нелюбимое число - 33."},
                        ] + [{"role": "user", "content": mes} for mes in messages],
                        stream=False
                    )

                    print(response.choices[0].message.content)
            else:
                res = json.loads(rec.PartialResult())["partial"]
                if res:
                    print(f"Поток: {res}")


if __name__ == "__main__":
    voce_listen()