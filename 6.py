import torch
import sounddevice as sd
import time
import torchaudio

speakers = ["aidar", "baya", "kseniya", "xenia", "eugene"]
for speaker in speakers:
    model = torch.package.PackageImporter(r".\v5_ru.pt").load_pickle("tts_models", "model")
    print(sd.query_devices())
    sd.default.device = 3
    audio = model.apply_tts(text="Прив+ет, друзь+я!", speaker=speaker, sample_rate=24000)
    sd.play(audio, 24000)
    time.sleep((len(audio) / 24000) + 0.5)
    sd.stop()
    torchaudio.save(f"{speaker}.mp3", audio.unsqueeze(0), sample_rate=24000)

    del audio
