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
import copy
import math


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
    
    def __init__(self, db, key="E",scale="major" ):
        self.db = db
        self.key = key
        self.scale = scale
        self.tick = 0

    def generate(self, tempo=120):
        print self.key, self.scale
        records = self.db.records_in_key_and_scale(self.key, self.scale)
        print "Working group size", len(records)
        result_pattern = midi.Pattern(resolution=480) 
        songs = []

        channels = [1,2]
        for channel in channels:
            track = None
            while track == None:
                uid = random.choice(records)["id"];
                pattern = self.db.pattern(uid)
                remapper = MidiRemapper("b0rkestra_description.json", pattern)
                midiutil.pattern_to_resolution(pattern, 480)
                pattern = remapper.remap_pattern(pattern)
                track = midiutil.get_track_from_pattern_with_channel(pattern, channel)
                if track:
                    print self.db.record(uid)["filename"]

            result_pattern.append(track)
            songs.append(pattern)
        return result_pattern

def loop_pattern(pattern, pattern_length, loop_count=4):
    was_rel = pattern.tick_relative
    if was_rel:
        pattern.make_ticks_abs()
    
    p_cache = copy.deepcopy(pattern)
    for i in range(loop_count):
        tick_skip = (i+1)*pattern_length
        p_add = copy.deepcopy(p_cache)
        
        for track in p_add:
            for event in track:
                event.tick += tick_skip

        for index, track in enumerate(pattern):
            track.extend(p_add[index])

    last_tick = midiutil.get_last_abs_tick_from_pattern(pattern)


    if was_rel:
        pattern.make_ticks_rel()




class Drummer:
    def __init__(self, drum_dir="mididrum-sample"):
        self.filenames = mididb.get_midi_filenames(drum_dir)
        self.patterns = [midi.read_midifile(filename) for filename in self.filenames]
        for p in self.patterns:
            midiutil.pattern_to_resolution(p, 480)
            midiutil.pattern_to_channel(p, 9)

            p.make_ticks_abs()

            #sanitize any wierd events
            for track in p:
                to_remove = []
                for event in track:
                    if not (event.name == "Note On" or event.name == "Note Off"):
                        to_remove.append(event)
                for event in to_remove:
                    track.remove(event)

            #Make all the drum loop samples roughly the same length
            bar_duration = midiutil.calculate_bar_duration(p)
            midiutil.trim_pattern_to_abs_tick(p, bar_duration)
            multiplier = int(round(bar_duration / float(midiutil.get_events_from_pattern(p, "Note On")[-1].tick)))

            if multiplier > 1.0:
                loop_pattern(p, bar_duration/multiplier, multiplier)
                #print "duration", bar_duration

            p.make_ticks_rel()

    def generate_bar(self):
        pattern = random.choice(self.patterns)
        return pattern




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




    patternMaker = PatternMaker2K(db, "E", "harmonic minor")
    pattern = patternMaker.generate()
    pattern = midiutil.get_bar_from_pattern(pattern, 10)


    drummer = Drummer()
    drums = drummer.generate_bar()
    drums = midiutil.get_bar_from_pattern(drums, 0)


    last_tick_drums  = midiutil.get_last_abs_tick_from_pattern(drums)
    print "last tick drums", last_tick_drums
    last_tick_pattern  = midiutil.get_last_abs_tick_from_pattern(pattern)
    print "last tick pattern", last_tick_pattern

    print "pattern bar duration: ", midiutil.calculate_bar_duration(pattern)
    print "drum bar duration:    ", midiutil.calculate_bar_duration(drums)



    #pattern = drums

    for track in drums:
        pattern.append(track)
    

    loop_pattern(pattern, midiutil.calculate_bar_duration(pattern), 3)

    #p = copy.deepcopy(pattern)
    #for i in range(4):
    #    for index, track in enumerate(pattern):
    #        track.extend(copy.deepcopy(p[index]))

    #record = db.find_by_filename("./midi-sample/Bruce_Springsteen_-_I'm_On_Fire.mid")
    #pattern = db.pattern(record[0]['id'])
    #result_pattern = midi.Pattern(resolution=480) 
    #result_pattern = pattern
    #track = midiutil.get_track_from_pattern_with_channel(pattern, 9)
    #midiutil.remove_events_of_name_from_track(track, "Note Off")



    # for event in track:
    #     if event.name =="Note On":
    #         #print event.tick
    #         #event.tick = int(event.tick/4.0)
    #         print event

    # result_pattern.append(track)
    # pattern = result_pattern







    #remapper = MidiRemapper("b0rkestra_description.json", pattern)


    seq = sequencer.SequencerWrite(sequencer_resolution=pattern.resolution)
    seq.subscribe_port(client, port)
    
    pattern.make_ticks_abs()
    



    events = []
    for track in pattern:
        for event in track:
            # event = remapper.remap(event)
            events.append(event)
    events.sort()



    seq.start_sequencer()
    for event in events:
        buf = seq.event_write(event, False, False, True)
        if buf == None:
            continue
        if buf < 1000:
            time.sleep(.005)
        while event.tick > seq.queue_get_tick_time():
            seq.drain()
            time.sleep(.005)


if __name__ == "__main__":
    main()