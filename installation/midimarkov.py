#!/usr/bin/env python
import json
import midi
import midiutil
import mididb
import random
import math
from itertools import tee, izip
from sets import Set


def nwise(iterable, n=2):
    group = tee(iterable,n)
    for i,it in enumerate(group):
        for a in range(i):
            next(it, None)
    return izip(*group)


class MarkovModel:
    def __init__(self):
        self.model = {}

    def add(self, state, next_state):
        if not state in self.model:
            self.model[state] = {next_state:1}
        else:
            if not next_state in self.model[state]:
                self.model[state][next_state] = 1
            else:
                self.model[state][next_state] += 1

    def weighted_random_nexstate(self, state):
        next_states = self.model[state]
        next_states = list(next_states.items())
        if (len(next_states) == 0): return None
        return self.__weighted_choice__( next_states)

    def random_state(self):
        choices = []
        for key in self.model:
            weight = 0
            for ns_key in self.model[key]:
                weight += self.model[key][ns_key]
            choice = (key, weight)
            choices.append(choice)
        print choices
        return self.__weighted_choice__(choices)

    def __weighted_choice__(self, choices):
        total = sum(w for c, w in choices)
        r = random.uniform(0, total)
        upto = 0
        for c, w in choices:
           if upto + w >= r:
              return c
           upto += w
        assert False, "Shouldn't get here"


def extract_midi_states(pattern, bar_duration=7680, states_per_bar=32):
    midiutil.pattern_to_resolution(pattern, 480)
    pattern.make_ticks_abs()
    #sanitize any wierd events
    for track in pattern:
        to_remove = []
        for event in track:
            if not (event.name == "Note On" or event.name == "Note Off"):
                to_remove.append(event)
        for event in to_remove:
            track.remove(event)

    #Make all the drum loop samples roughly the same length
    #midiutil.trim_pattern_to_abs_tick(pattern, bar_duration)
    multiplier = int(round(bar_duration / float(midiutil.get_events_from_pattern(pattern, "Note On")[-1].tick)))
    if multiplier > 1.0:
        midiutil.loop_pattern(pattern, bar_duration/multiplier, multiplier)

    events = []
    for track in pattern:
        for event in track:
            if event.name == "Note On":
                events.append(event)
    events.sort()

    states = []
    for i in xrange(states_per_bar):
        states.append([])

    for event in events:
        if event.tick >= bar_duration:
            continue
        state_num = int(math.floor(event.tick/float(bar_duration/states_per_bar)))
        states[state_num].append((event.tick - state_num*(bar_duration/states_per_bar), event.pitch))

    states = [tuple(state) for state in states]
    return states



def build_markov_model(dir="./mididrum-sample"):
    markov = MarkovModel()
    filenames = mididb.get_midi_filenames("./mididrum-sample/Funk Drums")
    #all_filenames = mididb.get_midi_filenames("./midi-sample")
    # filenames = []
    # for i in range(40):
    #     filenames.append(random.choice(all_filenames))


    for filename in filenames:
        if "fill" in filename.lower() or "break" in filename.lower():
            continue
        try:
            pattern = midi.read_midifile(filename)
        except:
            print "NO DICE"
            continue
        
        # pattern.make_ticks_abs()
        # no_drums = True
        # for track in pattern:
        #     to_remove = []
        #     for event in track:
        #         if event.name == "Note On":
        #             if event.channel == 9:
        #                 #print "BRING DA BIG DRUMS"
        #                 no_drums = False
        #         if (event.name == "Note On" or event.name == "Note Off") and event.channel != 9:
        #             to_remove.append(event)
        #     for event in to_remove:
        #         track.remove(event)
        # pattern.make_ticks_rel()
        # if no_drums:
        #     print "NO DICE"
        #     continue

        try:
            states = extract_midi_states(pattern, states_per_bar=32)
        except:
            print "NO DICE"
            continue
        for state, next_state in nwise(states, 2):
            markov.add(state, next_state)
        print "DRUMZZZZZ"

    return markov

def state_to_track(state,tick_offset=0, make_ticks_relative=False):
    track = midi.Track(tick_relative=False)
    for note in state:
        event = midi.NoteOnEvent(tick=note[0] + tick_offset, pitch=note[1], velocity=120)
        track.append(event)

    track.sort()

    if make_ticks_relative:
        track.make_ticks_rel()
    return track


def states_to_pattern(states, make_ticks_relative=True, bar_duration=7680, states_per_bar=32):
    pattern = midi.Pattern(tick_relative=False, resolution=480)
    track = midi.Track(tick_relative=False)

    for i, state in enumerate(states):
        tick_offset = i * (bar_duration/states_per_bar)
        track.extend(state_to_track(state,tick_offset=tick_offset))
    track.sort()
    pattern.append(track)
    if make_ticks_relative:
        pattern.make_ticks_rel()
    return pattern


def main():

    markov = build_markov_model()

    state = markov.random_state()
    count = 0
    states = []
    while state != None and count<128*2:
        print "OK"
        try:
            state = markov.weighted_random_nexstate(state)
        except KeyError:
            state = None
 
        if state != None:
            states.append(state)
        count += 1
    pattern = states_to_pattern(states)
    midi.write_midifile("output.mid", pattern)




if __name__ == '__main__':
    main()