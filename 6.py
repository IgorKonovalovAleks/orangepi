
import sounddevice as sd
import time
import torch
import torchaudio

print(sd.query_devices())
speaker = "aidar"
sample_rate = 24000
device = torch.device('cpu')  # cpu или gpu
torch.set_num_threads(4)  # количество задействованных потоков CPU

model = torch.package.PackageImporter("v5_ru.pt").load_pickle("tts_models", "model")

torch._C._jit_set_profiling_mode(False)
torch.set_grad_enabled(False)
model.to(device)
sd.default.device = 3


def speak(text: str):
    audio = model.apply_tts(text=text + "..",
                            speaker=speaker,
                            sample_rate=sample_rate,
                            )

    sd.play(audio, sample_rate)
    time.sleep((len(audio) / (sample_rate)) + 0.5)
    sd.stop()
    del audio  # освобождаем память


speak("Привет, друзья")
