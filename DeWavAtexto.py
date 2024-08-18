import wave
import subprocess
from pydub import AudioSegment
from vosk import Model, KaldiRecognizer


# Convertir el archivo a PCM 16kHz 16-bit mono usando ffmpeg
try:
    subprocess.run([
        'ffmpeg', '-i', 'audio.wav',
        '-ar', '16000',   # Cambiar la frecuencia de muestreo a 16 kHz
        '-ac', '1',       # Cambiar a un solo canal (mono)
        '-sample_fmt', 's16',  # Formato de muestra a 16 bits
        'converted_audio.wav'
    ], check=True)
except subprocess.CalledProcessError as e:
    print(f"Error al convertir el archivo de audio: {e}")
    exit(1)

# Abrir el archivo WAV convertido
try:
    wf = wave.open("converted_audio.wav", "rb")
except FileNotFoundError:
    print("El archivo de audio convertido no se encontró.")
    exit(1)

# Inicializar el modelo de reconocimiento de voz (En español)
model_path = "vosk-model-small-es-0.42"
try:
    model = Model(model_path)
except FileNotFoundError:
    print(f"Modelo de Vosk no encontrado en {model_path}.")
    exit(1)

# Crear un reconocedor
rec = KaldiRecognizer(model, wf.getframerate())

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
