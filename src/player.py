import pyaudio
import pydub
import numpy as np


class AudioPlayer:
    def __init__(self) -> None:
        self._volume_level = 0.5
        self._playback_speed = 1.0

        self._segment: pydub.AudioSegment = None
        self._array_sample = None
        self._current_idx = 0
        self._stream = None

    def open_file(self, file):
        self._segment = pydub.AudioSegment.from_file(file)
        self._array_sample = self._segment.get_array_of_samples()

    def play(self):
        self._current_idx = 0
        p = pyaudio.PyAudio() # TODO: move this to __init__ and close it in __del__

        def callback(in_data, frame_count, time_info, status):
            # print(f"seg.channels: {self._segment.channels}")
            # print(f"seg.frame_rate: {self._segment.frame_rate}")
            # print(f"seg.sample_width: {self._segment.sample_width}")

            # print(f"in_data: {in_data}")
            # print(f"frame_count: {frame_count}")
            # print(f"time_info: {time_info}")
            # print(f"status: {status}")
            # print(f"current_frame: {self._current_idx}")
            to_get = frame_count * self._segment.channels
            # print(f"to_get: {to_get}")
            data = self._array_sample[self._current_idx : self._current_idx + to_get]
            data = np.multiply(data, self._volume_level).astype(
                np.int16
            )  # TODO check if other types are supported
            self._current_idx = self._current_idx + to_get
            return (data.tobytes(), pyaudio.paContinue)

        self._stream = p.open(
            format=p.get_format_from_width(self._segment.sample_width),
            channels=self._segment.channels,
            # TODO find anorther way to speed up audio
            rate=round(self._segment.frame_rate * self._playback_speed), 
            output=True,
            stream_callback=callback,
        )

    def stop(self):
        self._stream.stop_stream()
        self._stream.close()

    def pause(self):
        self._stream.stop_stream()

    def resume(self):
        self._stream.start_stream()

    @property
    def volume(self, level):
        if level < 0.0 or level > 1.0:
            raise ValueError("Volume level must be between 0 and 1")
        self._volume_level = float(level)

    @property
    def playback_speed(self, speed):
        if speed < 0.0:
            raise ValueError("Playback speed must be positive")
        if speed > 4.0:
            raise ValueError("Playback speed must be less than 4.0")
        self._playback_speed = float(speed)

    def set_time(self, seconds):
        if seconds < 0:
            raise ValueError("Time must be positive")

        if seconds > self._segment.duration_seconds:
            raise ValueError("Time must be less than the duration of the audio")

        self._current_idx = int(
            self._segment.frame_rate * seconds * self._segment.channels
        )

    def get_time(self):
        return self._current_idx / (self._segment.frame_rate * self._segment.channels)

    def skip(self, seconds):
        self.set_time(self.get_time() + seconds)
        # while stream.is_active():
        #     time.sleep(0.1)
        # stream.stop_stream()
        # stream.close()


if __name__ == "__main__":
    import time

    player = AudioPlayer()

    player.open_file("test_data/Junior Jack - Luv 2 U.flac")
    player.play()  # Play audio of loaded file
    # time.sleep(5)
    player.volume = 0.2
    # time.sleep(5)

    player.pause()  # Pause audio

    # time.sleep(2)
    player.volume = 0.5

    player.resume()  # Resume audio

    # time.sleep(5)  # Wait for 5 seconds
    player.set_time(60 * 6 + 15)  # To the end of the track
    print(player.get_time())  # Get current time
    player.skip(-20)  # Skip 10 seconds back
    # time.sleep(5)
    player.skip(10)  # Skip 10 seconds ahead

    player.volume = 0.2
