import pandas
import numpy as np
from midiutil.MidiFile import MIDIFile

middle_c = 72
middle_csharp = middle_c + 1 
track    = 0
channel  = 0
time     = 0.00   # In beats
time_increment = 0.25
duration = 0.25   # In beats
tempo    = 120  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

framerate = 30

white_midi_deltas = [2, 2, 1, 2, 2, 2, 1]
black_midi_deltas = [2, 3, 2, 2, 3]
delta_reference = [0, 0, 1, 1, 2, 3, 2, 4, 2, 5, 4, 6]



##########################
## Import CSV File
##########################


piano_data = pandas.read_csv("data.csv", header=None).as_matrix()

middle_c_index = piano_data[0,0]
middle_csharp_index = piano_data[1,0]

print("Middle C is " + str(middle_c_index))
print("Middle C# is " + str(middle_csharp_index))
##################################
##FIND LOWEST WHITE KEY MIDI VALUE
##################################
octave_jumps = int(middle_c_index / 7)
low_c_index = middle_c_index - octave_jumps * 7

print("Lowest C is " + str(low_c_index))

tmp_index = low_c_index
low_white_midi = middle_c
i = 6
while tmp_index > 1:
    
    low_white_midi -= white_midi_deltas[i]
    i -= 1
    tmp_index -= 1

low_white_midi -= 12 * octave_jumps
print("Low White MIDI Value is " + str(low_white_midi))

##################################
##FIND LOWEST BLACK KEY MIDI VALUE
##################################
octave_jumps = int(middle_csharp_index / 5)
low_csharp_index = middle_csharp_index - octave_jumps * 5

print("Lowest C# is " + str(low_csharp_index))

tmp_index = low_csharp_index
low_black_midi = middle_csharp
i = 4
while tmp_index > 1:
        low_black_midi -= black_midi_deltas[i]
        i -=1
        tmp_index -=1
low_black_midi -= 12 * octave_jumps
print("Low Black MIDI Value is " + str(low_black_midi))

################################################################
##Get References Needed to Convert Piano Key array to midi array
##Have midi value of lowest note, and index to reference conversion
################################################################
if low_black_midi > low_white_midi:
    white_lowest = True
    lowest_note = low_white_midi
else:
    white_lowest = False
    lowest_note = low_black_midi

#####################################
##Convert Data to Midi Array
midi_array = np.empty((0,44), int)
##remove first two rows
piano_data = np.delete(piano_data, 0, 0)
piano_data = np.delete(piano_data, 0, 0)

while len(piano_data) > 0:
    curr_note = lowest_note
    current_frame = []
    white_keys = piano_data[0]
    black_keys = piano_data[1]
    curr_white_lowest = white_lowest
    while len(white_keys) > 0:
        if curr_white_lowest is True:
            current_frame.append(white_keys[0])
            white_keys = np.delete(white_keys, 0, 0)
            if white_midi_deltas[delta_reference[curr_note % 12]] == 2:
                curr_white_lowest = False
        else:
            current_frame.append(black_keys[0])
            black_keys = np.delete(black_keys, 0, 0)
            curr_white_lowest = True
        curr_note += 1
    current_frame.append(black_keys[0])
    print(current_frame)
    print("LENGTH OF FRAME " + str(len(current_frame)))
    print(midi_array.ndim)
    current_frame = np.array(current_frame)
    print(current_frame.ndim)
    midi_array = np.vstack([midi_array, current_frame])
    piano_data = np.delete(piano_data,0, 0)
    piano_data = np.delete(piano_data,0, 0)

midi_array = np.nan_to_num(midi_array)

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

for frame in midi_array:
    curr_note = lowest_note
    for note in frame:
        if int(note) == 1:
            print("Adding Note " + str(curr_note))
            MyMIDI.addNote(track, channel, curr_note, time, duration, volume)
        curr_note += 1
    time += 0.25


with open("output.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

