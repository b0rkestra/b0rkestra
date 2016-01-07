#!/usr/bin/env python
import midi
import sys
import PIL
import copy
import editdistance
import shelve
import StringIO
import midisanitize
import hashlib


def get_events_from_track(track, event_name):
    events = []
    for event in track:
        if event.name == event_name:
            events.append(event)
    return events


def get_events_from_pattern(pattern, event_name):
    events = []
    for track in pattern:
        filtered_track = get_events_from_track(track, event_name)
        events += filtered_track
    return events


def calculate_bar_duration(pattern):    
    time_signatures = get_events_from_pattern(pattern, "Time Signature")
    if len(time_signatures) == 0:
        raise IndexError("No time signatures in pattern")
    #just take the first time signature
    time_signature = time_signatures[0]
    bar_duration = pattern.resolution * time_signature.denominator * time_signature.numerator
    return bar_duration


def get_bar_from_pattern(pattern, bar_number):
    pattern = copy.deepcopy(pattern)
    bar_length = calculate_bar_duration(pattern)
    tick_offset = int(bar_number * bar_length)

    if pattern.tick_relative:
        pattern.make_ticks_abs()
    
    #time_signature = get_events_from_pattern(pattern, "Time Signature")[0]

    for track in pattern:
        to_remove = []
        #track_name = get_events_from_track(track, "Track Name")[0]

        for event in track:
            if event.tick >= tick_offset and event.tick < tick_offset + bar_length:
                event.tick -= tick_offset
            else:
                to_remove.append(event)

        for event in to_remove:
            track.remove(event)

        track.append(midi.EndOfTrackEvent(tick=bar_length-1))

    pattern.make_ticks_rel()
    return pattern


def get_track_events_at_tick(track, tick, name = None):
    originally_relative = track.tick_relative

    if originally_relative:
        track.make_ticks_abs()

    events = []
    for event in track:
        if event.tick == tick:
            if name == None:
                events.append(copy.deepcopy(event))
            else:
                if event.name == name:
                    events.append(copy.deepcopy(event))

    if originally_relative:
        track.make_ticks_abs()

    return events


def track_to_note_list(track):
    track = copy.deepcopy(track)
    track.make_ticks_abs()
    last_tick = 0
    if len(track) !=0:
        last_tick = track[-1].tick
    track_note_list = []

    for tick in range(last_tick):
        events = get_track_events_at_tick(track, tick, "Note On")
        notes = [event.pitch for event in events if hasattr(event, 'pitch')]
        notes.sort()
        #notes = ''.join(notes)
        track_note_list.append(notes)

    return track_note_list


def visualise_pattern(pattern):
    num_tracks = len(pattern)


def get_track_name(track):
    name = [ event.text for event in get_events_from_track(track, "Track Name")]
    if len(name) == 0:
        name = ""
    else:
        name = name[0]
    return name


def get_track_info(pattern):
    info = []

    for index, track in enumerate(pattern):
        track_info = {"index":index}
        name = get_track_name(track)
        track_info["name"] = name
        info.append(track_info)
    
    return info


def track_timing_similarity(track_a, track_b):
    note_list1 = track_to_note_list(track_a)
    note_list2 = track_to_note_list(track_b)
    if len(note_list1) != len(note_list2):
        raise IndexError("Tracks must be the same number of ticks")
    
    diff_sum = 0
    for notes in zip(note_list1, note_list2):
        diff_sum += editdistance.eval(notes[0], notes[1])

    return diff_sum

def pattern_timing_similarity(pattern_a, pattern_b):
    if len(pattern_a) != len(pattern_b):
        raise IndexError("Patterns must have the same number of tracks")

    error_sum = 0
    for track_a, track_b in zip(pattern_a, pattern_b):
        error_sum += track_timing_similarity(track_a, track_b)
    return error_sum


# Song Database Record
# {
#     id:"MD5Hash_of_data",
#     filename: "filename.mid",
#     data:binary_file_data,
#     track_names: ["drums","guitar","synth", "bass"],
#     tempo:127,
#     time_signature:[numerator, denominator],
#     ticks_per_bar:840,
#     ticks_per_quarter_note:86,
#     tick_length: 1000000,
#     split_bars:[
#         {"id":"MD5hash_of_data", "data":binary_bar_data, "name":"bar_number"}
#     ],
#     split_tracks:[
#         {"id":"MD5hash_of_data", "data":binary_track_data, "name":"track_name"}
#     ],
#     split_bars_tracks:[
#         [binary_track0_bar0, binary_track1_bar0]
#     ]
# }


def print_events(pattern, exclude=["Note On"]):
    for track in pattern:
        for event in track:
            if not event.name in exclude:
                print event.name
                print event


def main():
    #pattern1 = midi.read_midifile("midi/5RAP_04.MID")
    bars = []
    pattern = midi.read_midifile("midi/5RAP_04.MID")
    #pattern = midi.read_midifile("midi/decoy.mid")
    #pattern = midi.read_midifile("midi/drum_patterns.mid")

    print_events(pattern)
    pattern = midisanitize.sanitize(pattern)

    midi.write_midifile("test.mid", pattern)
    return
    #pattern2 = midi.read_midifile("midi/5RAP_05W.MID")

    for i in range(5):
        print "Extracting Bar", i
        bars.append(get_bar_from_pattern(pattern, i))

    test_bar = bars[3]
    similarity = []
    for bar in bars:
        similar = pattern_timing_similarity(test_bar, bar)
        similarity.append({"similarity":similar, "bar":bar})


    similarity.sort(key=lambda x:x["similarity"], reverse=True)
    for result in similarity:
        print result["similarity"]

    #print get_track_info(pattern1)
    #bar1 = get_bar_from_pattern(pattern1, 0)
    #bar2 = get_bar_from_pattern(pattern2, 0)
    #print track_timing_similarity(bar1[0], bar2[0])


    #print len(note_list1)
    #print len(note_list2)

    #print note_list1

    #print track_to_note_list(bar1[0])
    #print track_to_note_list(bar2[0])

    output = StringIO.StringIO()
    midi.write_midifile(output, pattern)
    print output



if __name__ == "__main__":
    main()