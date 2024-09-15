"""PyAudio Example: Play a wave file (callback version)."""

import wave
import time
import pyaudio
import pydub
import tempfile
import numpy as np


file = "test_data/Junior Jack - Luv 2 U.flac"
# file = "test_data/Belfast - Orbital.wav"
# file = "test_data/Onipa - Fire (Edit) (Mixed).mp3"
# file = "test_data/100Hz_44100Hz_16bit_30sec.mp3"

print(f"Playing {file}")
# Convert the file to wave format using pydub
wave_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
pydub.AudioSegment.from_file(file).export(wave_file.name, format="wav")

# if len(sys.argv) < 2:
#     print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
#     sys.exit(-1)
volume = 0.5
segment = pydub.AudioSegment.from_file(file)
arraysample = segment.get_array_of_samples()


with wave.open(wave_file.name, "rb") as wf:
    current_frame = 0
    # with wave.open(file, 'rb') as wf:
    # Define callback for playback (1)
    def callback(in_data, frame_count, time_info, status):
        global current_frame

        print(f"wf.getnchannels(): {wf.getnchannels()}")
        print(f"wf.getframerate(): {wf.getframerate()}")
        print(f"wf.getsampwidth(): {wf.getsampwidth()}")
        
        print(f"in_data: {in_data}")
        print(f"frame_count: {frame_count}")
        print(f"time_info: {time_info}")
        print(f"status: {status}")
        print(f"current_frame: {current_frame}")
        data = wf.readframes(frame_count)
        print(f"len(data): {len(data)}")
        current_frame = current_frame + frame_count
        data_np = np.frombuffer(data, dtype=np.int16)
        data_np = (data_np * volume).astype(np.int16)

        # pydub.AudioSegment(data)
        # If len(data) is less than requested frame_count, PyAudio automatically
        # assumes the stream is finished, and the stream stops.
        return (data_np.tobytes(), pyaudio.paContinue)

    # Instantiate PyAudio and initialize PortAudio system resources (2)
    p = pyaudio.PyAudio()

    # Open stream using callback (3)
    
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        stream_callback=callback,
    )

    # Wait for stream to finish (4)
    while stream.is_active():
        time.sleep(0.1)
    # stream.stop_stream() # Pause the stream
    # stream.start_stream() # Resume the stream

    # Close the stream (5)
    stream.close()

    # Release PortAudio system resources (6)
    p.terminate()

wave_file.close()
