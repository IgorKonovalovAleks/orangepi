import gtts

a = gtts.gTTS(text="Привет", lang='ru')
a.save('h.mp3')
