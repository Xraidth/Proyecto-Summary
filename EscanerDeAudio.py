import vosk
import wave

# Inicializar el modelo de reconocimiento de voz (En español)
model = vosk.Model("./vosk-model-small-es-0.42") 

# Abrir el archivo de audio
wf = wave.open("your_audio_file.wav", "rb")

# Crear un reconocedor
rec = vosk.KaldiRecognizer(model, wf.getframerate())

# Procesar el audio
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())

print(rec.FinalResult())  
