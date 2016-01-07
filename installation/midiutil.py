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
