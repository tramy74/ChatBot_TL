# backend/app/utils/video_transcription.py
from moviepy.editor import VideoFileClip
import speech_recognition as sr
import os

def transcribe_video_audio(video_path):
    """
    Extracts audio from a video file and transcribes it to text.
    
    :param video_path: Path to the video file
    :return: Transcribed text as a string
    """
    # Extract audio from video
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)  # Save audio to a temporary file

    # Initialize the speech recognizer
    recognizer = sr.Recognizer()
    transcript = ""

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)  # Read entire audio file
        try:
            # Recognize speech using Google Web Speech API
            transcript = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")

    # Clean up temporary audio file
    os.remove(audio_path)
    
    return transcript
