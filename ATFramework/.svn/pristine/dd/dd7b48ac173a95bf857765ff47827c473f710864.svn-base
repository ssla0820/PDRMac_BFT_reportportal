from sys import byteorder
from array import array
from struct import pack
import pyaudio
import wave
import platform
from ..log import logger

# ==========================================================================
# Support Windows Only now (2022/05)
# Record audio from System Stereo Mixer (for Windows 10 & 11)
#
# **Please make sure the Stereo Mix recording device is enabled First.**
# Reference: https://techcult.com/how-to-enable-stereo-mix-on-windows-10/
# ==========================================================================


class AudioCapture:
    def __init__(self, sample_rate=44100, silent_threshold=100):
        self.sample_rate = sample_rate
        self.silent_threshold = silent_threshold # original: 500, the value is lower than 10 if real silent
        self.format = pyaudio.paInt16
        self.chunk_size = int(self.sample_rate/10) # default: 1024
        self.channels = 2

    @staticmethod
    def get_stereo_mix_device_id():
        p = pyaudio.PyAudio()
        curr_device_id = -1
        device_list = ['Stereo Mix', '立體聲混音', 'CABLE']  # Add "CABLE" for virtual device, 2022/8/1 update by Volath
        if platform.system() == 'Darwin':
            device_list = ['BlackHole'] # For macOS, install BlackHole 2ch for routing audio
        logger(f'device list={device_list}')
        for i in range(0, p.get_device_count()):
            for dev_name in device_list:
                if dev_name in p.get_device_info_by_index(i)['name']:
                    curr_device_id = i
                    break
            if not curr_device_id == -1:
                break
        logger(f'device id={curr_device_id}')
        return curr_device_id

    def is_silent(self, snd_data):
        # "Returns 'True' if below the 'silent' threshold"
        return max(snd_data) < self.silent_threshold

    @staticmethod
    def normalize(snd_data):
        # "Average the volume out"
        maximum = 16384
        times = float(maximum) / max(abs(i) for i in snd_data)

        r = array('h')
        for i in snd_data:
            r.append(int(i * times))
        return r

    def trim(self, snd_data):
        "Trim the blank spots at the start and end"

        def _trim(snd_data):
            snd_started = False
            r = array('h')

            for i in snd_data:
                if not snd_started and abs(i) > self.silent_threshold:
                    snd_started = True
                    r.append(i)

                elif snd_started:
                    r.append(i)
            return r

        # Trim to the left
        snd_data = _trim(snd_data)

        # Trim to the right
        snd_data.reverse()
        snd_data = _trim(snd_data)
        snd_data.reverse()
        return snd_data

    def add_silence(self, snd_data, seconds):
        # "Add silence to the start and end of 'snd_data' of length 'seconds' (float)"
        silence = [0] * int(seconds * self.sample_rate)
        r = array('h', silence)
        r.extend(snd_data)
        r.extend(silence)
        return r

    def record(self, duration=10): # duration: the duration to record (sec)
        """
        Record a word or words from the microphone and
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the
        start and end, and pads with 0.5 seconds of
        blank sound to make sure VLC et al can play
        it without getting chopped off.
        """
        p = pyaudio.PyAudio()

        # device_id = 2
        device_id = self.get_stereo_mix_device_id()
        device_info = p.get_device_info_by_index(device_id)  # check the system sound device id by
        channels = device_info["maxInputChannels"] if (
                device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info[
            "maxOutputChannels"]
        self.channels = channels  # sync self.channels as device's default channels, 2022/8/1 update by Volath
        logger(f'{device_info=}, {channels=}, {self.channels=}')

        # https://people.csail.mit.edu/hubert/pyaudio/docs/#pyaudio.Stream.__init__
        stream = p.open(format=self.format,
                        channels=channels,
                        rate=int(device_info["defaultSampleRate"]),
                        input=True,
                        frames_per_buffer=self.chunk_size,
                        input_device_index=device_info["index"]
                        )

        num_silent = 0
        snd_started = False
        duration_silent_auto_stop = int(int(device_info["defaultSampleRate"] / self.chunk_size)) * 3  # frames

        r = array('h')
        curr_record_frames = 0
        # 2022-07-04: for fixing macOS the first frame is not silent (not start to play audio) after first time recording
        has_dropped_first_frame = False

        while True:
            # little endian, signed short
            snd_data = array('h', stream.read(self.chunk_size))
            if byteorder == 'big':
                snd_data.byteswap()
            # r.extend(snd_data)

            silent = self.is_silent(snd_data)
            if not has_dropped_first_frame:
                has_dropped_first_frame = True
                continue

            if not silent and snd_started:  # reset num_silent (by Jim)
                num_silent = 0

            if silent and snd_started:
                num_silent += 1
            elif not silent and not snd_started:
                snd_started = True

            if snd_started:
                r.extend(snd_data)
                curr_record_frames += self.chunk_size
                if curr_record_frames > int(device_info["defaultSampleRate"]) * duration:
                    logger(f'Record finish. {curr_record_frames=}')
                    break

            if snd_started and num_silent > duration_silent_auto_stop:  # for auto-stop recording
                break

        sample_width = p.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        p.terminate()

        r = self.normalize(r)
        r = self.trim(r)
        # r = self.add_silence(r, 0.5)
        return sample_width, r

    def record_to_file(self, file_path, duration=10):
        # "Records from the microphone and outputs the resulting data to 'path'"
        logger(f'record_to_file - Start')
        sample_width, data = self.record(duration)
        data = pack('<' + ('h' * len(data)), *data)

        wf = wave.open(file_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(sample_width)
        wf.setframerate(self.sample_rate)
        wf.writeframes(data)
        wf.close()
        logger(f'record_to_file - End')