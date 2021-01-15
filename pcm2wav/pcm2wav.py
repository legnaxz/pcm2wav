import os
import sys
import wave
import librosa
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

if len(sys.argv) == 6:
    WorkDirectoryPath = sys.argv[1]
    Channels = int(sys.argv[2])
    BitDepth = int(sys.argv[3])
    SampleRate = int(sys.argv[4])
    ResampleRate = int(sys.argv[5])
else:
    WorkDirectoryPath = os.getcwd()
    Channels = 1
    BitDepth = 16
    SampleRate = 16000
    ResampleRate = 16000

WaveDirectoryPath = WorkDirectoryPath + "_wav_original"
ResampleDirectoryPath = WorkDirectoryPath + "_wav_resample"
if not os.path.exists(WaveDirectoryPath):
    os.makedirs(WaveDirectoryPath)

print("WorkDirectoryPath : ", WorkDirectoryPath)
print("Channels : ", Channels)
print("BitDepth : ", BitDepth)
print("SampleRate : ", SampleRate)
print("ResampleRate : ", ResampleRate)


def pcm2wav(pcm_file, wav_file, channels=1, bit_depth=16, sampling_rate=16000):

    # Check if the options are valid.
    if bit_depth % 8 != 0:
        raise ValueError("bit_depth "+str(bit_depth) +
                         " must be a multiple of 8.")

    # Read the .pcm file as a binary file and store the data to pcm_data
    with open(pcm_file, 'rb') as opened_pcm_file:
        pcm_data = opened_pcm_file.read()

        obj2write = wave.open(wav_file, 'wb')
        obj2write.setnchannels(channels)
        obj2write.setsampwidth(bit_depth // 8)
        obj2write.setframerate(sampling_rate)
        obj2write.writeframes(pcm_data)
        obj2write.close()


def LoadPCMFiles(pcm_path, wav_path, resample_path):
    for files in os.listdir(pcm_path):
        if os.path.isdir(os.path.join(pcm_path, files)):
            if not os.path.exists(os.path.join(wav_path, files)):
                os.makedirs(os.path.join(wav_path, files))

            if not os.path.exists(os.path.join(resample_path, files)):
                os.makedirs(os.path.join(resample_path, files))

            LoadPCMFiles(os.path.join(pcm_path, files),
                         os.path.join(wav_path, files),
                         os.path.join(resample_path, files)
                         )
        else:
            pcm_dir = os.path.join(pcm_path, files)

            if '.pcm' in files:
                wave_dir = os.path.join(
                    wav_path, files.replace('.pcm', '.wav'))
                # resample_files = 'resample_' + files.replace('.pcm', '.wav')
                # resample_wav_dir = os.path.join(resample_path, resample_files)
                resample_wav_dir = os.path.join(
                    resample_path,  files.replace('.pcm', '.wav'))
                pcm2wav(pcm_dir, wave_dir, Channels, BitDepth, SampleRate)
                down_sample(wave_dir, resample_wav_dir,
                            SampleRate, ResampleRate)

            elif '.PCM' in files:
                wave_dir = os.path.join(
                    wav_path, files.replace('.PCM', '.wav'))
                # resample_files = 'resample_' + files.replace('.PCM', '.wav')
                # resample_wav_dir = os.path.join(resample_path, resample_files)
                resample_wav_dir = os.path.join(
                    resample_path,  files.replace('.PCM', '.wav'))
                pcm2wav(pcm_dir, wave_dir, Channels, BitDepth, SampleRate)
                down_sample(wave_dir, resample_wav_dir,
                            SampleRate, ResampleRate)


def down_sample(input_wav, output_wav, origin_sr, resample_sr):
    y, sr = librosa.load(input_wav, sr=origin_sr)
    resample = librosa.resample(y, sr, resample_sr)

    sf.write(output_wav, resample, resample_sr,
             format='wav', endian='LITTLE', subtype='PCM_16')


if __name__ == "__main__":
    LoadPCMFiles(WorkDirectoryPath, WaveDirectoryPath, ResampleDirectoryPath)
    print("Done")
