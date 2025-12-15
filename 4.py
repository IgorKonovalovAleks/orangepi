import torch

language = 'ru'
model_id = 'v5_ru'
device = torch.device('cpu')
model, example_text = torch.hub.load(repo_or_dir='snakers4/silero-models',
                                     model='silero_tts',
                                     language=language,
                                     speaker=model_id)
model.to(device)  # gpu or cpu
sample_rate = 48000
speaker = 'xenia'
put_accent=True
put_yo=True
put_stress_homo=True
put_yo_homo=True

example_text = 'Меня зовут Лева Королев. Я из готов. И я уже готов открыть все ваши замки любой сложности!'

audio = model.apply_tts(text=example_text,
                        speaker=speaker,
                        sample_rate=sample_rate,
                        put_accent=put_accent,
                        put_yo=put_yo,
                        put_stress_homo=put_stress_homo,
                        put_yo_homo=put_yo_homo)

ssml_sample = """
              <speak>
              <p>
                  Когда я просыпаюсь, <prosody rate="x-slow">я говорю довольно медленно</prosody>.
                  Потом я начинаю говорить своим обычным голосом,
                  <prosody pitch="x-high"> а могу говорить тоном выше </prosody>,
                  или <prosody pitch="x-low">наоборот, ниже</prosody>.
                  Потом, если повезет – <prosody rate="fast">я могу говорить и довольно быстро.</prosody>
                  А еще я умею делать паузы любой длины, например, две секунды <break time="2000ms"/>.
                  <p>
                    Также я умею делать паузы между параграфами.
                  </p>
                  <p>
                    <s>И также я умею делать паузы между предложениями</s>
                    <s>Вот например как сейчас</s>
                  </p>
              </p>
              </speak>
              """

audio = model.apply_tts(ssml_text=ssml_sample,
                        speaker=speaker,
                        sample_rate=sample_rate)