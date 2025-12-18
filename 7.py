from gtts import gTTS
from io import BytesIO
import soundfile as sf
import sounddevice as sd

fp = BytesIO()
gTTS("Привет друзья", lang="ru").write_to_fp(fp)
fp.seek(0)
data, fs = sf.read(fp, dtype="float32")

sd.play(data, fs)
sd.wait()
