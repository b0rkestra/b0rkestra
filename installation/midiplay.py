#!/usr/bin/env python
import sys
import time
import midi
import mididb
import random
import midi.sequencer as sequencer
from midiremap import MidiRemapper
import mididb
import midiutil
import threading

class MidiPlayer(threading.Thread):
    def __init__(self, pattern_queue, resolution=480, client=14, port=0):
        threading.Thread.__init__(self)
        self.pattern_queue = pattern_queue
        self.seq = sequencer.SequencerWrite(sequencer_resolution=resolution)
        self.seq.subscribe_port(client, port)


    def run(self):
        pattern.make_ticks_abs()
        events = []
        for track in pattern:
            for event in track:
                event = remapper.remap(event)
                events.append(event)
        events.sort()
        self.seq.start_sequencer()
        for event in events:
            buf = self.seq.event_write(event, False, False, True)
            if buf == None:
                continue
            if buf < 1000:
                time.sleep(.5)
            while event.tick > self.seq.queue_get_tick_time():
                self.seq.drain()
                time.sleep(.5)


class PatternMaker2K:
    
    def __init__(self, db, key="E",scale="Major" ):
        self.db = db
        self.key = key
        self.scale = scale
        self.tick = 0

    def generate(self, ):
        pass




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



    db = mididb.MidiDB();
    print db.__key_index__.keys()
    print db.__scale_index__.keys()


    records = db.records_in_key_and_scale("C", 'minor')
    print "Working group size", len(records)
    result_pattern = midi.Pattern(resolution=480) 
    songs = []

    channels = [2,1,9,1]
    for channel in channels:
        track = None
        
        while track == None:
            uid = random.choice(records)["id"];
            pattern = db.pattern(uid)
            remapper = MidiRemapper("b0rkestra_description.json", pattern)
            midiutil.pattern_to_resolution(pattern, 480)
            pattern = remapper.remap_pattern(pattern)


            track = midiutil.get_track_from_pattern_with_channel(pattern, channel)

        result_pattern.append(track)
        songs.append(pattern)

    #print pattern
    #result_pattern = db.pattern(random.choice(records)["id"])

    remapper = MidiRemapper("b0rkestra_description.json", result_pattern)
    #remapper.remap_pattern(result_pattern)
    pattern = result_pattern

    #filenames = mididb.get_midi_filenames("./midi-sample")
    #filename = random.choice(filenames)
    #print("Playing", filename)
    #pattern = midi.read_midifile(filename)
    #remapper = MidiRemapper("b0rkestra_description.json", pattern)


    seq = sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)
    
    pattern.make_ticks_abs()
    
    for event in pattern[2]:
        event.tick = int(event.tick/1.5)


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