import sys
from moviepy.editor import VideoFileClip
from speech_recognition import Recognizer, AudioFile
from textwrap import fill


def transcribe_video(video_path, output_file, segment_length=3):
    """
    Transcribes a video, splitting audio into segments and saving transcripts.

    Args:
        video_path (str): Path to the video file.
        output_file (str): Path to save the combined transcript text file.
        segment_length (int, optional): Segment duration in minutes (default: 10).
    """

    # Extract and split audio
    clip = VideoFileClip(video_path)
    audio = clip.audio
    segment_length *= 60
    num_segments = int(audio.duration / segment_length)
    segments = []
    for segment in range(num_segments):
        start_time = segment * segment_length
        end_time = (segment + 1) * segment_length
        segments.append(audio.subclip(start_time, end_time))

    remaining_start = num_segments * segment_length
    remaining_audio = audio.subclip(remaining_start)
    segments.append(remaining_audio)

    # Transcribe each segment and write to separate files
    print(len(segments))
    segment_transcripts = []
    for i, segment in enumerate(segments):
        segment_path = f"audio_{i+1}.wav"
        segment.write_audiofile(segment_path)
        recognizer = Recognizer()
        with AudioFile(segment_path) as source:
            audio = recognizer.record(source)
        transcription = recognizer.recognize_google(audio)
        segment_transcripts.append(transcription)
        sys.wait(3)

    # Combine transcripts and write to output file
    combined_transcript = "\n\n".join(
        fill(text, width=100) for text in segment_transcripts
    )
    with open(output_file, "w") as f:
        f.write(combined_transcript)

    print(f"Transcription saved to: {output_file}")


# Example usage
video_path = "QClass - QKD - Lecture 3_ Entanglement Based QKD & Security Analysis.mp4"
output_file = "transcription.txt"

transcribe_video(video_path, output_file)
