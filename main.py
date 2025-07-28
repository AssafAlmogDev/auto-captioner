import os
os.environ["IMAGEMAGICK_BINARY"] = r"C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\magick.exe"

import whisper
from moviepy.editor import AudioFileClip, TextClip, CompositeVideoClip

# Configuration
audio_filename = "voice.mp3"
video_width, video_height = 1280, 720
font_size = 70
font_name = "Arial-Bold"

# Load Whisper model and transcribe with word timestamps
model = whisper.load_model("base")
result = model.transcribe(audio_filename, word_timestamps=True)

# Extract words with timestamps
words = []
for segment in result['segments']:
    for word in segment['words']:
        words.append({
            "text": word['word'].strip(),
            "start": word['start'],
            "end": word['end']
        })

# Load audio clip
audio_clip = AudioFileClip(audio_filename)
duration = audio_clip.duration

# Create text clips with stroke using ImageMagick
clips = []
for w in words:
    txt_clip = (
        TextClip(
            w['text'],
            fontsize=font_size,
            font=font_name,
            color='white',
            stroke_color='black',
            stroke_width=2,
            method='label'  # Use ImageMagick rendering
        )
        .set_position('center')
        .set_start(w['start'])
        .set_duration(w['end'] - w['start'])
    )
    clips.append(txt_clip)

# Compose final video
final_video = CompositeVideoClip(clips, size=(video_width, video_height)).set_duration(duration)
final_video = final_video.set_audio(audio_clip)

# Export to file
final_video.write_videofile("output.mp4", fps=24)
