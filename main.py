import pytube
from transformers import pipeline
import moviepy.editor as mp
import librosa
import io
import ffmpeg

# Stream del video
yt = pytube.YouTube("https://www.youtube.com/watch?v=9-GjBYvOFyw")
audio_stream = yt.streams.filter(only_audio=True).first().url

# Inicializa el transcriptor y el resumidor
transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-large")
summarizer = pipeline("summarization")

# Transcripción y resumen en tiempo real
def process_audio_stream(audio_stream_url):
    # Utiliza ffmpeg para capturar el audio en tiempo real
    process = (
        ffmpeg
        .input(audio_stream_url)
        .output('pipe:', format='wav', acodec='pcm_s16le', ac=1, ar='16k')
        .run_async(pipe_stdout=True)
    )
    
    audio_buffer = io.BytesIO()

    while True:
        in_bytes = process.stdout.read(4096)
        if not in_bytes:
            break
        audio_buffer.write(in_bytes)
        
        # Procesar el audio en fragmentos
        audio_buffer.seek(0)
        audio, sample_rate = librosa.load(audio_buffer, sr=16000)
        transcription = transcriber(audio, sampling_rate=sample_rate)

        # Generar resumen para cada fragmento transcrito
        summary = summarizer(transcription["text"], max_length=130)
        print(summary)
        
        
        audio_buffer.seek(0)
        audio_buffer.truncate(0)

    process.wait()

# Procesa el audio en streaming
process_audio_stream(audio_stream)


