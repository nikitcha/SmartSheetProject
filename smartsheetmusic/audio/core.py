from . import helpers

def wav():
    midi_obj = helpers.load_midi()
    wav_obj = helpers.midi_to_wav(midi_obj)
    return wav_obj
    
def play(wav_obj):
    helpers.play(wav_obj)
    
def stop():
    helpers.stop()    