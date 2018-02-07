import numpy as np
import sounddevice as sd
import pretty_midi
import librosa

# Audio Constants
SAMPLE_RATE = 11025
HOP_SIZE = 1024
BUFFER_SIZE = 10 # in seconds
FRAMES_IN_BUFFER  = SAMPLE_RATE*BUFFER_SIZE
FEATURES_IN_BUFFER = int(SAMPLE_RATE*BUFFER_SIZE/HOP_SIZE)
CHANNELS = 1
INSTRUMENT = 0
SOUNDFONT = br"./data/WeedsGM3.sf2"
FEATUREMODE = 'cqt' 

def wave_callback(micwav, indata, frames, time, status):  
    micwav = np.append(micwav, indata)
    if micwav.shape[0]>FEATURES_IN_BUFFER:
        micwav = micwav[-FEATURES_IN_BUFFER:]
    return micwav
            

def get_mic():     
    mic = sd.InputStream(channels=CHANNELS, 
                   callback=wave_callback,
                   samplerate=SAMPLE_RATE)
    return mic


def load_midi(midifile=None):
    if midifile is None:
        midifile = './data/Chopin Nocturne op9 no2.mid'
    midi_obj = pretty_midi.PrettyMIDI(midifile)
    for instrument in midi_obj.instruments:        
        instrument.program = INSTRUMENT
    return midi_obj

def midi_to_wav(midi_obj):
    wav_obj = midi_obj.fluidsynth(fs=SAMPLE_RATE, sf2_path = SOUNDFONT)
    return wav_obj
    
def wav_to_features(wav_obj):
    if FEATUREMODE =='cqt':
        features = librosa.feature.chroma_cqt(y=wav_obj,sr=SAMPLE_RATE, hop_length=HOP_SIZE, norm = 2, threshold=0, n_chroma=8*12, n_octaves=8, fmin = 16.5)
    elif FEATUREMODE == 'cens':
        features = librosa.feature.chroma_cens(y=wav_obj,sr=SAMPLE_RATE, hop_length=HOP_SIZE, norm = 2, n_chroma=7*12, n_octaves=7)
    elif FEATUREMODE == 'stft':
        features = librosa.feature.chroma_stft(y=wav_obj,sr=SAMPLE_RATE, hop_length=HOP_SIZE, norm = 2, n_chroma=8*12)
    elif FEATUREMODE == 'mel':
        features = librosa.feature.melspectrogram(y=wav_obj,sr=SAMPLE_RATE, hop_length=HOP_SIZE)
    elif FEATUREMODE == 'mfcc':
        features = librosa.feature.mfcc(y=wav_obj,sr=SAMPLE_RATE, hop_length=HOP_SIZE, n_mfcc=8*12)
    elif FEATUREMODE == 'poly':
        features = librosa.feature.poly_features(y=wav_obj,sr=SAMPLE_RATE, hop_length=HOP_SIZE)
    return features
    
def play(wav_obj):
    sd.play(wav_obj, SAMPLE_RATE)

def stop():
    sd.stop()