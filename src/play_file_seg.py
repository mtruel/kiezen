"""PyAudio Example: Play a wave file (callback version)."""

import time
import pyaudio
import pydub
import numpy as np

file = "test_data/Junior Jack - Luv 2 U.flac"
# file = "test_data/Belfast - Orbital.wav"
# file = "test_data/Onipa - Fire (Edit) (Mixed).mp3"
# file = "test_data/100Hz_44100Hz_16bit_30sec.mp3"
# file = "test_data/100Hz_44100Hz_16bit_30sec_96.mp3"
# file = "test_data/Free_Test_Data_500KB_MP3.mp3"
print(f"Playing {file}")


volume = 0.5
segment = pydub.AudioSegment.from_file(file)
# arraysample_bin = segment.get_array_of_samples()
# arraysample = np.frombuffer(arraysample_bin, dtype=np.int16)

arraysample = segment.get_array_of_samples()

def _play_with_pyaudio(seg):
    current_idx = 0

    def callback(in_data, frame_count, time_info, status):
        nonlocal current_idx
        print(f"seg.channels: {seg.channels}")
        print(f"seg.frame_rate: {seg.frame_rate}")
        print(f"seg.sample_width: {seg.sample_width}")

        print(f"in_data: {in_data}")
        print(f"frame_count: {frame_count}")
        print(f"time_info: {time_info}")
        print(f"status: {status}")
        print(f"current_frame: {current_idx}")
        # data = next(get_frames(frame_count))
        to_get = frame_count * seg.channels # * seg.sample_width
        data = arraysample[current_idx : current_idx + to_get]
        # print(f"len(data): {len(data)}")
        # data_np = np.frombuffer(data, dtype=np.int16)
        # data = (data * volume).astype(np.int8)
        data = np.multiply(data, volume).astype(np.int16)
        current_idx = current_idx + to_get

        # assumes the stream is finished, and the stream stops.
        return (data.tobytes(), pyaudio.paContinue)

    p = pyaudio.PyAudio()

    # Just in case there were any exceptions/interrupts, we release the resource
    stream = p.open(
        format=p.get_format_from_width(seg.sample_width),
        channels=seg.channels,
        rate=round(seg.frame_rate * 1.),
        output=True,
        stream_callback=callback,
    )
    # So as not to raise OSError: Device Unavailable should play() be used again
    while stream.is_active():
        time.sleep(0.1)
    try:
        pass
        # break audio into half-second chunks (to allows keyboard interrupts)
        #     data_np = np.frombuffer(chunk._data, dtype=np.int16)
        #     data_np = (data_np * volume).astype(np.int16)
        #     stream.write(data_np.tobytes())
    finally:
        print("Closing stream")
        stream.stop_stream()
        stream.close()

        p.terminate()


_play_with_pyaudio(segment)
