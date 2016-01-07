#!/usr/bin/env python
import copy
import midi
import math
import midiutil


def __make_consistent_time_signature__(pattern):
    print ("Making consitent time signature")
    time_signatures = midiutil.get_events_from_pattern(pattern, "Time Signature")
    if len(time_signatures) == 0:
        raise IndexError("No time signatures in pattern")
    to_remove = time_signatures[1:]
    for track in pattern:
        midiutil.remove_events_from_track(track, to_remove)

        
def __make_consistent_tempo__(pattern):
    print ("Making consitent tempo")
    tempos = midiutil.get_events_from_pattern(pattern, "Set Tempo")
    if len(tempos) == 0:
        raise IndexError("No tempos in pattern")
    to_remove = tempos[1:]
    for track in pattern:
        midiutil.remove_events_from_track(track, to_remove)


def __name_all_tracks__(pattern):
    print ("Naming all tracks")
    
    for index, track in enumerate(pattern):
        names = midiutil.get_events_from_track(track, "Track Name")
        if len(names) == 0:
            name = "Track "+str(index)
            name_event = midi.TrackNameEvent(tick=0, text=name)
            track.insert(0, name_event)
            print "    naming track at index", index, "\""+name+"\""
        else:
            if names[0].text == '':
                names[0].text = "Track "+str(index)
            midiutil.remove_events_from_track(track, names[1:])


def __make_all_tracks_integer_bar_multiple__(pattern):
    print ("Making all tracks integer bar length")
    bar_duration = midiutil.calculate_bar_duration(pattern)
    print "    bar duration", bar_duration

    orignally_ticks_relative = pattern.tick_relative
    if pattern.tick_relative:
        pattern.make_ticks_abs()

    longest_tick = 0
    eot_events = []
    for track in pattern:
        eot_events += midiutil.get_events_from_track(track, "End of Track")

    eot_events.sort(key=lambda x:x.tick, reverse=True)
    last_tick = eot_events[0].tick

    bar_number = int(math.ceil(float(last_tick)/float(bar_duration)))
    print "    number of bars", bar_number
    tick_length = bar_number * bar_duration

    for event in eot_events:
        event.tick = tick_length

    if orignally_ticks_relative:
        pattern.make_ticks_rel()


def sanitize(pattern):
    pattern = copy.deepcopy(pattern)
    __make_consistent_time_signature__(pattern)
    __make_consistent_tempo__(pattern)
    __name_all_tracks__(pattern)
    __make_all_tracks_integer_bar_multiple__(pattern)
    return pattern


def main():
    #pattern1 = midi.read_midifile("midi/5RAP_04.MID")
    bars = []
    pattern = midi.read_midifile("midi/5RAP_04.MID")
    #pattern = midi.read_midifile("midi/decoy.mid")
    #pattern = midi.read_midifile("midi/drum_patterns.mid")

    #print_events(pattern, [])
    pattern = sanitize(pattern)

    midi.write_midifile("test.mid", pattern)
    pattern = midi.read_midifile("test.mid")
    print pattern
    return

if __name__ == "__main__":
    main()