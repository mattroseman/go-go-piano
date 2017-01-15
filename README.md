# go-go-piano
piano video image processing to convert to sheet music

## What is it?
go-go-piano is designed to take videos of piano playing, determine what keys are being pressed using image processing, and then convert the pressed key data into a highly adaptable MIDI file which can easily be converted to sheet music and played back.

## What does it use?
- The raw frames of the videos are brought into Matlab, where the program is able to process and output to a CSV File
- CSV Data is imported into a python program which will determine what keys relate to what notes and convert the data into a MIDI file
- The MIDI file can then be imported into Musescore and played or LilyPond and converted into sheet music

## How does it work?
- An initial frame of the piano without anything blocking the keys (hands) is determine the bounds of the piano and each black and white key
- Data sets of hands on a piano are used to determine where the hands in the video are and the hands are masked out
- Each frame is compared to the first frame to watch for lighting differences on keys.  If it passes the threshold, the key is recorded as pressed
- The Middle C and Middle C# Key are determined based on location on the piano, and their indexes are recorded.
- Data is outputted into a CSV file, with the first two lines indicating the index of Middle C and Middle C#.  Additional lines are binary arrays of white and black keys for each frame, with a 1 indicating a key being pressed
- CSV data is imported into a Python program, where the program determines the note of the bottom-most key
- Keys are assigned MIDI note values
- Each frame is checked to find key presses and durations, and frames are converted to 1/16, 1/8, 1/4, 1/2, or whole notes.
- Notes are outputted into a MIDI file

## Difficulties With the Project
Difficulties included determining the best method to filter out false positive and false negative key presses, not having enough data to reliably model hands, and lining up the MIDI score evenly
 
## Future ideas
This technology could be further improved to analyze what fingers press what keys, and determine how good / bad hand posture is.  In addition, processing time could be decreased by only checking keys that are near the player's hands, rather than the entire keyboard every frame.

