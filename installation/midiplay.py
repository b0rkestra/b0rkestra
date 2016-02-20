#!/usr/bin/env python
import sys
import time
import midi
import mididb
import random
import midi.sequencer as sequencer
from midiremap import MidiRemapper


def main():
	client = 0
	port = 0
	if len(sys.argv) != 3:
		s = sequencer.SequencerHardware()
		print s
		client = int(raw_input('client number --> '))
		port = int(raw_input('port number --> '))
		print client, port
	else:
		client = sys.argv[1]
		port = sys.argv[2]

	filenames = mididb.get_midi_filenames("./midi-sample")
	filename = random.choice(filenames)
	print("Playing", filename)
	pattern = midi.read_midifile(filename)


	remapper = MidiRemapper("b0rkestra_description.json", pattern)



	seq = sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
	seq.subscribe_port(client, port)
	
	pattern.make_ticks_abs()
	events = []
	for track in pattern:
	    for event in track:
	    	event = remapper.remap(event)
	        events.append(event)
	events.sort()
	seq.start_sequencer()
	for event in events:
	    buf = seq.event_write(event, False, False, True)
	    if buf == None:
	        continue
	    if buf < 1000:
	        time.sleep(.5)
	while event.tick > seq.queue_get_tick_time():
	    seq.drain()
	    time.sleep(.5)


if __name__ == "__main__":
	main()