from moviepy.editor import AudioFileClip

# Cargar el archivo de audio
audio_clip = AudioFileClip("./audio.webm")

# Establecer la tasa de muestreo a 16 kHz
audio_clip = audio_clip.set_fps(16000)

# Guardar el archivo de audio en un nuevo archivo con codec PCM 16-bit
audio_clip.write_audiofile("audio2.wav", codec='pcm_s16le')
