#!/usr/bin/env python
import midi
import math
import sys
import PIL
import copy
import editdistance
import shelve
import StringIO
import midisanitize
import hashlib
import operator

def midi_to_file_object(pattern):
    output_file = StringIO.StringIO()
    midi.write_midifile(output_file, pattern)
    return output_file


def midi_to_data(pattern):
    return midi_to_file_object(pattern).getvalue()


def data_to_midi(data):
    pattern = midi.read_midifile(StringIO.StringIO(data))
    return pattern


def get_events_from_track(track, event_name):
    events = []
    for event in track:
        if event.name == event_name:
            events.append(event)
    return events


def remove_events_from_track(track, events):
    for event in events:
        try:
            track.remove(event)
            print "    removing", event
        except ValueError:
            pass


def get_events_from_pattern(pattern, event_name):
    events = []
    for track in pattern:
        filtered_track = get_events_from_track(track, event_name)
        events += filtered_track
    return events


def remove_events_of_name_from_pattern(pattern, name):
    for track in pattern:
        to_remove = []
        for event in track:
            if event.name == name:
                to_remove.append(event)
        for event in to_remove:
            track.remove(event)


def calculate_bar_duration(pattern):    
    time_signatures = get_events_from_pattern(pattern, "Time Signature")
    if len(time_signatures) == 0:
        raise IndexError("No time signatures in pattern")
    #just take the first time signature
    time_signature = time_signatures[0]
    bar_duration = pattern.resolution * time_signature.denominator * time_signature.numerator
    return bar_duration



def split_tracks_to_patterns(pattern):
    tempo = get_events_from_pattern(pattern, "Set Tempo")[0]
    time_signature = get_events_from_pattern(pattern, "Time Signature")[0]

    track_patterns = []

    for track in pattern:
        track_pattern = midi.Pattern()
        add_tempo = False
        add_time_signature = False
        new_tempo = copy.deepcopy(tempo)
        new_time_signature = copy.deepcopy(time_signature)

        if len(get_events_from_track(track, "Set Tempo")) ==0:
            add_tempo = True

        if len(get_events_from_track(track, "Time Signature")) ==0:
            add_time_signature = True

        track = copy.deepcopy(track)
        if add_tempo:
            track.insert(0, new_tempo)
        if add_time_signature:
            track.insert(0, new_time_signature)
        track_pattern.append(track)
        track_patterns.append(track_pattern)

    return track_patterns


def get_bar_from_pattern(pattern, bar_number):
    pattern = copy.deepcopy(pattern)
    bar_length = calculate_bar_duration(pattern)
    tick_offset = int(bar_number * bar_length)

    if pattern.tick_relative:
        pattern.make_ticks_abs()
    
    #time_signature = get_events_from_pattern(pattern, "Time Signature")[0]

    for track in pattern:
        to_remove = []
        track_name = get_events_from_track(track, "Track Name")[0]
        track_name.tick = 0
        tempo = get_events_from_track(track, "Set Tempo")[0]
        tempo.tick = 0
        time_signature = get_events_from_track(track, "Time Signature")[0]
        time_signature.tick = 0

        for event in track:
            if event.tick >= tick_offset and event.tick < tick_offset + bar_length:
                event.tick -= tick_offset
            else:
                to_remove.append(event)

        for event in to_remove:
            track.remove(event)

        track.append(midi.EndOfTrackEvent(tick=bar_length-1))
        track.insert(0, track_name)
        track.insert(0, tempo)
        track.insert(0, time_signature)

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

def get_track_names(pattern):
    names = []
    for track in pattern:
        names.append(get_track_name(track))
    return names


def get_track_info(pattern):
    info = []

    for index, track in enumerate(pattern):
        track_info = {"index":index}
        name = get_track_name(track)
        track_info["name"] = name
        info.append(track_info)
    
    return info


def get_time_signature(pattern, default_time_signature = [4,4]):
    time_signature = default_time_signature
    time_sigs = get_events_from_pattern(pattern, "Time Signature")
    if len(time_sigs) > 0:
        time_signature = [time_sigs[0].numerator, time_sigs[0].denominator] 
    return time_signature


def get_tempo(pattern, default_tempo=127.0):
    tempo = default_tempo
    tempos = get_events_from_pattern(pattern, "Set Tempo")
    if len(tempos) > 0:
        mpqn =tempos[0].mpqn 
        tempo = mpqn/6000.0
        tempo = (60*1000000)/float(mpqn)
    return tempo


def note_to_number(note):
    octave = int(''.join(filter(lambda x: x.isdigit(), note)))
    note_name = ''.join(filter(lambda x: (not x.isdigit()), note))
    note_to_number_lookup = {"C":0, "C_s":1, "D":2, "D_s":3, "E":4, "F":5, "F_s":6, "G":7, "G_s":8, "A":9, "A_s":10, "B":11}
    return note_to_number_lookup[note_name] + octave*12


def number_to_note(number):
    number_to_note_lookup = {0:"C", 1:"C_s", 2:"D", 3:"D_s", 4:"E", 5:"F", 6:"F_s", 7:"G", 8:"G_s", 9:"A", 10:"A_s", 11:"B"}
    note_name = number_to_note_lookup[number%12]
    octave = str(int(math.floor(number/12.0)))
    return note_name+octave


def get_note_distribution(pattern, ignored_channels=[], ignore_octave=True):

    notes = []
    if type(pattern).__name__ == "Pattern":
        notes = get_events_from_pattern(pattern, "Note On")
    elif type(pattern).__name__ == "Track":
        notes = get_events_from_track(pattern, "Note On")


    distribution = {}
    if ignore_octave:
        distribution = {"C":0, "C_s":0, "D":0, "D_s":0, "E":0, "F":0, "F_s":0, "G":0, "G_s":0, "A":0, "A_s":0, "B":0}


    for note in notes:
        if note.channel in ignored_channels:
            continue
        
        note_name = number_to_note(note.pitch)

        if ignore_octave:
            note_name = number_to_note(note.pitch%12)
            note_name = ''.join(filter(lambda x: (not x.isdigit()), note_name))

        if note_name in distribution:
            distribution[note_name] += 1
        else:
            distribution[note_name] = 1

        #pitch = note_to_number(note_name)
        #print note.pitch, note.pitch%12, note_name, pitch 
    return distribution


musical_scales = {
    "major"             :[2,2,1,2,2,2,1],
    "ionian"            :[2,2,1,2,2,2,1],
    "minor"             :[2,1,2,2,1,2,2],
    "aeolian"           :[2,1,2,2,1,2,2],
    "harmonic minor"    :[2,1,2,2,1,3,1],
    "jazz minor"        :[2,1,2,2,2,2,1],
    "melodic minor"     :[2,1,2,2,2,2,1],
    "dorian"            :[2,1,2,2,2,1,2],
    "dorian b2"         :[1,2,2,2,2,1,2],
    "phrigian #6"       :[1,2,2,2,2,1,2],
    "phrigian"          :[1,2,2,2,1,2,2],
    "phrigian dominant" :[1,3,1,2,1,2,2],
    "spanish"           :[1,3,1,2,1,2,2],
    "lydian"            :[2,2,2,1,2,2,1],
}
def generate_scale(root, name):
    notes = [root]
    for skip in musical_scales[name]:
        notes.append(notes[-1] + skip)
    return notes



def generate_note_range(root,num_notes):
    if isinstance(root, basestring):
        root = note_to_number(root)
    notes = []
    for i in range(num_notes):
        notes.append(root + i)
    return notes

def numbers_to_notes(numbers):
    result = []
    for number in numbers:
        result.append(number_to_note(number))
    return result

def notes_to_numbers(notes):
    result = []
    for note in notes:
        result.append(note_to_number(note))
    return result


def fit_track_to_note_range(track, range_root, range_num_note=24):
    pass


def print_key_scale_notes(root):
    for scale in musical_scales.keys():
        notes = generate_scale(note_to_number(root+'0'), scale)
        notes = numbers_to_notes(notes)
        print scale, notes[0], notes[3], notes[4]


def guess_scale(root, distribution=None):
    notes = []
    for note in distribution.keys():
        notes.append(note+'0')
    notes.sort()



    results = {}
    for scale_name in musical_scales.keys():
        test_notes = generate_scale(note_to_number(root+'0'), scale_name)
        test_notes = numbers_to_notes(test_notes)
        test_notes.sort()
        diff_notes = list(set(notes).difference(set(test_notes)))
        diff_notes = [n[:-1] for n in diff_notes]
        error_sum = sum( distribution[n] for n in diff_notes)
        #results[scale_name] = error_sum
        try: 
            results[error_sum].append(scale_name)
        except KeyError:
            results[error_sum] = [scale_name]
    
    diff_counts = results.keys()
    diff_counts.sort()
    return results[diff_counts[0]]


def guess_key(pattern, distribution=None):
    if distribution == None:
        distribution = get_note_distribution(pattern, [9])
    root = max(distribution.iteritems(), key=operator.itemgetter(1))[0]
    #guess_scale(root, distribution)
    #print numbers_to_notes(generate_scale(note_to_number(root+'0'), "major"))
    #print numbers_to_notes(generate_scale(note_to_number(root+'0'), "minor"))
    #print_key_scale_notes(root)

    #editdistance.eval(notes[0], notes[1])

    return root


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


def print_events(pattern, exclude=["Note On"]):
    for track in pattern:
        for event in track:
            if not event.name in exclude:
                print event.name
                print event

def pattern_to_resolution(pattern, resolution=480):
    current_resolution = pattern.resolution
    res_multiplier = float(resolution / current_resolution)
    for track in pattern:
        for event in track:
            event.tick = int(res_multiplier*event.tick)
    pattern.resolution = resolution