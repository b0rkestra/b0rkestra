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
import Queue
import copy
import math


class MidiPlayer(threading.Thread):
    def __init__(self, bar_size = 7680,resolution=480, client=14, port=0):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.event_queue = Queue.Queue()
        self.seq = sequencer.SequencerWrite(sequencer_resolution=resolution)
        self.seq.subscribe_port(client, port)
        self.bar_size = bar_size
        self.last_tick = 0
        self.current_tick = 0

    def append_bar(self, pattern):
        pattern = copy.deepcopy(pattern)
        pattern.make_ticks_abs()
        midiutil.trim_pattern_to_abs_tick(pattern, self.bar_size)

        event_list =[]
        for track in pattern:
            for event in track:
                event.tick += self.last_tick
                event_list.append(event)
        
        event_list.sort()

        for event in event_list:
            if event.name == "Note On" or event.name == "Note Off":
                self.event_queue.put(event)


        self.last_tick += self.bar_size


    def run(self):  
        self.seq.start_sequencer()
        print dir(self.seq)
        while True:
            if self.event_queue.empty():
                time.sleep(0.05)
                continue

            event = self.event_queue.get()
            buf = self.seq.event_write(event, False, False, True)
            if buf == None:
                continue
            if buf < 1000:
                time.sleep(.005)
            while event.tick > self.seq.queue_get_tick_time():
                self.current_tick = self.seq.queue_get_tick_time()
                self.seq.drain()
                time.sleep(.005)
        print "Queue empty"


class PatternMaker2K:
    def __init__(self, db, key="E",scale="major" ):
        self.db = db
        self.key = key
        self.scale = scale
        self.tick = 0

    def sample_random_bar(self, tempo=120, channels = [1,2,3]):
        print self.key, self.scale
        records = self.db.records_in_key_and_scale(self.key, self.scale)
        print "Working group size", len(records)
        result_pattern = midi.Pattern(resolution=480) 
        for channel in channels:
            track = None
            loop_count = 0
            while track == None:
                uid = random.choice(records)["id"];
                pattern = self.db.pattern(uid)
                remapper = MidiRemapper("b0rkestra_description.json", pattern)
                midiutil.pattern_to_resolution(pattern, 480)
                pattern = remapper.remap_pattern(pattern)
                track = midiutil.get_track_from_pattern_with_channel(pattern, channel)
                if track:
                    print self.db.record(uid)["filename"]
                loop_count += 1

            result_pattern.append(track)

        #result_pattern = midiutil.get_bar_from_pattern(result_pattern, random.choice(range(0,10)))
        return result_pattern

    def generate_bar(self, instrument_channels =[1,2,3]):
        result_pattern = self.sample_random_bar(channels = instrument_channels)
        midiutil.turn_notes_off_in_pattern(result_pattern)
        return result_pattern




class BassMan(PatternMaker2K):
    def __init__(self, db, key="E", scale="major",instrument_channels=[1]):
        PatternMaker2K.__init__(self, db, key, scale)
        self.groove_a = self.sample_random_bar(channels=instrument_channels)
        self.groove_b = self.sample_random_bar(channels=instrument_channels)
        self.groove_transition = [0.0, 0.0, 1.0, 0.0]
        self.groove_position = 0
        self.instrument_channels = instrument_channels

    def generate_bar(self):
        result_pattern = midi.Pattern(resolution=self.groove_a.resolution)

        self.groove_a.make_ticks_abs()
        self.groove_b.make_ticks_abs()
        for i in range(max(len(self.groove_a), len(self.groove_b))):
            result_pattern.append(midi.Track())
        result_pattern.make_ticks_abs()

        for track_index, track in enumerate(self.groove_a):
            for event in track:
                if random.random()  < 1.0 - (self.groove_transition[self.groove_position]):
                    result_pattern[track_index].append(copy.deepcopy(event))


        for track_index, track in enumerate(self.groove_b):
            for event in track:
                if random.random()  < (self.groove_transition[self.groove_position]):
                    result_pattern[track_index].append(copy.deepcopy(event))
        for track in result_pattern:
            track.sort()


        self.groove_a.make_ticks_rel()
        self.groove_b.make_ticks_rel()
        result_pattern.make_ticks_rel()

        self.groove_position += 1
        if self.groove_position >= len(self.groove_transition):
            self.groove_a = self.groove_b
            self.groove_b = self.sample_random_bar(channels=self.instrument_channels)
            self.groove_position = 0


        #result_pattern = midiutil.get_bar_from_pattern(result_pattern, random.choice(range(0,18)))
        midiutil.turn_notes_off_in_pattern(result_pattern)
        return result_pattern



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
                midiutil.loop_pattern(p, bar_duration/multiplier, multiplier)
                #print "duration", bar_duration

            p.make_ticks_rel()
        
        self.drum_change_probability = 0.1
        self.fill_probability = 0.2
        self.current_pattern = random.choice(self.patterns)

    def generate_bar(self):
        if random.random() < self.drum_change_probability:
            self.current_pattern = random.choice(self.patterns)

        pattern = self.current_pattern

        if random.random() < self.fill_probability:
            print "QUEUE DRUM FILL"
            pattern = random.choice(self.patterns)

        pattern = midiutil.get_bar_from_pattern(pattern, 0)
        midiutil.turn_notes_off_in_pattern(pattern)
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


    key = "D"
    scale = "harmonic minor"



    racketPatternMaker = PatternMaker2K(db, key, scale)
    pattern = racketPatternMaker.generate_bar([2])
    print "Got initial racket pattern"

    tubulumPatternMaker = PatternMaker2K(db, key, scale)
    tubulum = tubulumPatternMaker.generate_bar([3])
    print "Got initial tubulum pattern"


    drummer = Drummer()
    drums = drummer.generate_bar()
    print "Got initial drummer pattern"


    bass_man = BassMan(db, key, scale)
    bass = bass_man.generate_bar()
    print "Got initial bass pattern"


    pattern.extend(drums)
    pattern.extend(bass)
    pattern.extend(tubulum)



    midi_player = MidiPlayer(client=client, port=port)
    midiutil.turn_notes_off_in_pattern(pattern)
    midi_player.append_bar(pattern)
    midi_player.start()

    while threading.active_count() > 0:
        print midi_player.last_tick, midi_player.current_tick


        if midi_player.current_tick > midi_player.last_tick - 5000:

            
            print "Getting racketc"
            pattern = racketPatternMaker.generate_bar([2])
            pattern = midiutil.get_bar_from_pattern(pattern, 0)
            midiutil.turn_notes_off_in_pattern(pattern)
            

            print "Getting bass"
            bass = bass_man.generate_bar()
            bass = midiutil.get_bar_from_pattern(bass, 0)
            midiutil.turn_notes_off_in_pattern(bass)

            print "Getting drums"
            drums = drummer.generate_bar()
            drums = midiutil.get_bar_from_pattern(drums, 0)
            midiutil.turn_notes_off_in_pattern(drums)

            print "Getting tubulum"
            tubulum = tubulumPatternMaker.generate_bar([3])
            tubulum = midiutil.get_bar_from_pattern(tubulum, 0)
            midiutil.turn_notes_off_in_pattern(tubulum)


            pattern.extend(drums)
            pattern.extend(bass)
            pattern.extend(tubulum)



            midiutil.turn_notes_off_in_pattern(pattern)

            midi_player.append_bar(pattern)
            midi_player.append_bar(pattern)

        time.sleep(0.1)
    midi_player.join()
    return

    


if __name__ == "__main__":
    main()