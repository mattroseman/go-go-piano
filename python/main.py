import pandas
import numpy as np
from midiutil.MidiFile import MIDIFile

middle_c = 72
middle_csharp = middle_c + 1 
track    = 0
channel  = 0
time     = 0.50   # In beats
time_increment = 0.25
duration = 0.25   # In beats
tempo    = 120  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

framerate = 10


quarter_frames = framerate/(tempo/60)
sixteenth_frames = round(quarter_frames / 4)
eighth_frames = sixteenth_frames * 2
quarter_frames = eighth_frames * 2
half_frames = quarter_frames * 2
whole_frames = half_frames * 2

print(quarter_frames)
print(sixteenth_frames)
print(eighth_frames)
print(half_frames)


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
midi_array = None
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
    current_frame = np.array(current_frame)
    if midi_array is None:
        midi_array = np.empty((0,len(current_frame)), int)

    midi_array = np.vstack([midi_array, current_frame])
    piano_data = np.delete(piano_data,0, 0)
    piano_data = np.delete(piano_data,0, 0)

midi_array = np.nan_to_num(midi_array)

MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
                     # automatically created)
MyMIDI.addTempo(track,time, tempo)

frame = 0
note = 0


while frame < len(midi_array):
    #print("FRAME: " + str(frame))
    curr_note = lowest_note
    while note < len(midi_array[frame]):
        length = 0
        ahead = 0
        while frame + ahead < len(midi_array) and int(midi_array[frame + ahead,note]) == 1 :
            midi_array[frame + ahead, note] = 0
            #print("NOTE " + str(curr_note) + " AT FRAME " + str(frame + ahead))
            length += 1
            ahead += 1
        if length >= sixteenth_frames:
            #duration = 0.25
            if length >= eighth_frames:
                #duration = 0.5
                if length >= quarter_frames:
                    duration = 1
                    if length >= half_frames:
                       duration = 2
                       if length >= quarter_frames + half_frames:
                           duration = 3
                           if length >= whole_frames:
                               duration = 4

            print("Adding Note " + str(curr_note) + " of len " + str(duration) + " at beat " + str(time))
            MyMIDI.addNote(track, channel, curr_note, time, duration, volume)
        elif length > 0:
            print("NOTE NOT LONG ENOUGH LENGTH IS " + str(length))
        curr_note += 1
        note += 1
    note = 0
    frame += 1
    if frame % sixteenth_frames == 0:
        time += .25


with open("output.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

print(quarter_frames)
