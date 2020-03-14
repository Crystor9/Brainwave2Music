import csv

import numpy as np
import MidiFile as md
# import fluidsynth as fl
# from midi2audio import FluidSynth

meanFrequencies = []
numChannels = 1
with open('nothing.csv') as csvfile:
    next(csvfile)
    next(csvfile)
    reader = csv.reader(csvfile)

    prevFrequencies = np.zeros(5)
    count = 0.0
    for line in reader:
        frequencies = np.array(line[3:8]).astype(np.float)

        if count >= 128.0 / 4.3:
            temp = np.array(prevFrequencies[0: numChannels])
            meanFrequencies.append(temp/ count)
            prevFrequencies = frequencies
            count = 1.0
        else:
            prevFrequencies += frequencies
            count += 1.0

meanFrequencies = np.array(meanFrequencies).astype(int)
degrees = []

for f in meanFrequencies:
    degrees.append(f % 4000 % 40 + 40)

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
tempo = 260  # In BPM
volume = 80  # 0-127, as per the MIDI standard

MyMIDI = md.MIDIFile(numChannels) # number of tracks are equal to the number of EEG channels
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    for j in range(numChannels):
        MyMIDI.addNote(track + j, channel + j, pitch[j], time + i, duration, volume)


with open("nothing-AF3.mid", "wb") as output_file:
    MyMIDI.writeFile(output_file)

# FluidSynth().play_midi("C:\\Users\\ratan\\Documents\\pitchTest.mid")
