import time
from tkinter import messagebox
from moviepy.editor import VideoFileClip
from speech_recognition import Recognizer, AudioFile
from textwrap import fill
from tkinter import *
from tkinter import filedialog
import threading


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
        time.sleep(3)

    # Combine transcripts and write to output file
    combined_transcript = "\n\n".join(
        fill(text, width=100) for text in segment_transcripts
    )
    with open(output_file, "w") as f:
        f.write(combined_transcript)

    print(f"Transcription saved to: {output_file}")


# Example usage
# video_path = "QClass - QKD - Lecture 3_ Entanglement Based QKD & Security Analysis.mp4"
# output_file = "transcription.txt"

# transcribe_video(video_path, output_file)


def Widgets():

    source_label = Label(root, text="Video  :", pady=5, padx=5)
    source_label.grid(row=2, column=0, pady=5, padx=5)

    root.source_Text = Entry(root, width=35, textvariable=video_path, font="Arial 14")
    root.source_Text.grid(row=2, column=1, pady=5, padx=5, columnspan=2)

    destination_label = Label(root, text="Destination :", pady=5, padx=9)
    destination_label.grid(row=3, column=0, pady=5, padx=5)

    root.destinationText = Entry(
        root, width=27, textvariable=dest_path, font="Arial 14"
    )
    root.destinationText.grid(row=3, column=1, pady=5, padx=5)

    browse_B1 = Button(
        root, text="Browse Vid", command=Browse_vid, width=10, relief=GROOVE
    )
    browse_B1.grid(row=2, column=2, pady=1, padx=1)
    browse_B2 = Button(
        root, text="Browse path", command=Browse_path, width=10, relief=GROOVE
    )
    browse_B2.grid(row=3, column=2, pady=1, padx=1)

    TranscribeB = Button(
        root,
        text="Transcribe Video",
        command=start_transcribe_video,
        width=20,
        pady=10,
        padx=15,
        relief=GROOVE,
        font="Georgia, 13",
    )
    TranscribeB.grid(row=5, column=1, pady=10, padx=10)


def Browse_vid():

    path = filedialog.askopenfilename(
        initialdir="YOUR DIRECTORY PATH", title="choose Video"
    )

    video_path.set(path)


def Browse_path():

    dir = filedialog.askdirectory(
        initialdir="YOUR DIRECTORY PATH", title="Save textfile"
    )

    dest_path.set(dir)


def start_transcribe_video():
    transcribe_label = Label(root, text="In Progress...", pady=5, padx=9)
    transcribe_label.grid(row=9, column=0, pady=5, padx=5)

    t1 = threading.Thread(
        target=transcribe_video,
        args=(video_path.get(), dest_path.get() + "transcribe.txt"),
    )
    t1.start()


root = Tk()


root.geometry("520x250")
root.resizable(False, False)
root.title("Video transcriber")

video_path = StringVar()
dest_path = StringVar()

Widgets()


root.mainloop()
