import csv

import numpy as np
import MidiFile as md
import sys

meanFrequencies = []
with open(sys.argv[1]) as csvfile:
    next(csvfile)
    next(csvfile)
    reader = csv.reader(csvfile)

    prevFrequencies = np.zeros(5)
    count = 0.0
    for line in reader:
        frequencies = np.array(line[3:8]).astype(np.float)

        if count == 128.0 / 8:
            meanFrequencies.append(prevFrequencies[0] / count)
            prevFrequencies = frequencies
            count = 1.0
        else:
            prevFrequencies += frequencies
            count += 1.0

meanFrequencies = np.array(meanFrequencies)
degrees = []

for f in meanFrequencies:
    degrees.append((int(f % 4000) % 40 + 40))

track = 0
channel = 0
time = 0  # In beats
duration = 1  # In beats
tempo = 260  # In BPM
volume = 80  # 0-127, as per the MIDI standard

MyMIDI = md.MIDIFile(1)  # One track, defaults to format 1 (tempo track is created automatically)
MyMIDI.addTempo(track, time, tempo)

for i, pitch in enumerate(degrees):
    MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

with open(sys.argv[2], "wb") as output_file:
    MyMIDI.writeFile(output_file)
