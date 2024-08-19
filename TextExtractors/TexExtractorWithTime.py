from youtube_transcript_api import YouTubeTranscriptApi
import os
os.system('cls')

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

def get_transcription_with_timestamps_youtube_api(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
    
    for entry in transcript:
        start_time = entry['start']
        duration = entry['duration']
        end_time = start_time + duration
        text = entry['text']
        formatted_start_time = format_time(start_time)
        formatted_end_time = format_time(end_time)
        print(f"{text}, {formatted_start_time} - {formatted_end_time}")

# Extraer ID del video de la URL
URL = "https://www.youtube.com/watch?v=9-GjBYvOFyw"
video_id = URL.replace("https://www.youtube.com/watch?v=","")

get_transcription_with_timestamps_youtube_api(video_id)


