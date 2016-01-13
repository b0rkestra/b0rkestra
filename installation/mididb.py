#!/usr/bin/env python
import hashlib
import midi
import midisanitize
import midiutil
import StringIO
import shelve
import json
import copy
import base64
import os


def generate_id(f):
    hash = hashlib.md5()
    #f = open(fname, "rb") 
    if type(f) == StringIO.StringIO:
        hash.update(f.getvalue())
    else:
        hash.update(f.read())

    f.close()
    return hash.hexdigest()

def generate_id_from_data(data):
    hash = hashlib.md5()
    hash.update(data)
    return hash.hexdigest()



def create_record(filename):
    print "## Creating record", filename
    print "### Sanitizing"
    record = {}
    record["filename"] = filename
    record["id"] = generate_id(open(filename, "rb"))

    pattern = midi.read_midifile("midi/5RAP_04.MID")
    pattern = midisanitize.sanitize(pattern)
    
    record["data"] = midiutil.midi_to_data(pattern)
    record["ticks_per_bar"] = midiutil.calculate_bar_duration(pattern)
    pattern.make_ticks_abs()
    record["max_tick"] = pattern[0][-1].tick
    pattern.make_ticks_rel()

    record["track_names"] = midiutil.get_track_names(pattern)

    record["bars"] = []
    print "### Splitting to Bars"
    for bar in range(record["max_tick"]/record["ticks_per_bar"]):
        bar_pattern = midiutil.get_bar_from_pattern(pattern, bar)
        bar_id = generate_id_from_data(midiutil.midi_to_data(bar_pattern))
        bar = {"name": str(bar), "id":bar_id, "data":midiutil.midi_to_data(bar_pattern)}
        record["bars"].append(bar)
    
    record["tracks"] = []
    tracks = midiutil.split_tracks_to_patterns(pattern)
    print "### Splitting to Tracks"
    for index, name in enumerate(record["track_names"]):
        track_pattern = tracks[index]
        track_id = generate_id_from_data(midiutil.midi_to_data(track_pattern))
        track = {"name": name, "data":midiutil.midi_to_data(track_pattern)}
        record["tracks"].append(track)

    record["bars_tracks"] = []
    print "### Splitting to Tracks and Bars"
    for bar in range(record["max_tick"]/record["ticks_per_bar"]):
        bar_pattern = midiutil.get_bar_from_pattern(pattern, bar)
        tracks = midiutil.split_tracks_to_patterns(bar_pattern)
        
        for index, name in enumerate(record["track_names"]):
            bar_track_pattern = tracks[index]
            bars_tracks_id = generate_id_from_data(midiutil.midi_to_data(bar_track_pattern))
            bar_track = {"name": "track:"+name+" bar:"+str(bar), "id":bars_tracks_id, "data":midiutil.midi_to_data(bar_track_pattern)}
            record["bars_tracks"].append(bar_track)

    return record


def record_to_json(record):
    record = copy.deepcopy(record)
    record["data"] = base64.b64encode(record["data"])

    for bar in record["bars"]:
        bar["data"] = base64.b64encode(bar["data"])

    for track in record["tracks"]:
        track["data"] = base64.b64encode(track["data"])
    return json.dumps(record)


def json_to_record(json_record):
    record = json.loads(json_record)
    record["data"] = base64.b64decode(record["data"])

    for bar in record["bars"]:
        bar["data"] = base64.b64decode(bar["data"])

    for track in record["tracks"]:
        track["data"] = base64.b64decode(track["data"])
    return record

def get_midi_filenames(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        path = root
        for filename in files:
            filename = os.path.join(path, filename)
            tmp, extension = os.path.splitext(filename)
            if extension.lower() == '.mid':    
                filenames.append(filename)
    return filenames


def load(filename="midi.shelve"):
    shelve_midi_db = shelve.open(filename)
    return shelve_midi_db



def id_pattern_itter(db):
    for record in db["records"]:
        record = db["records"][record]
        yield (record["id"], midi.read_midifile(StringIO.StringIO(record["data"])))
        for bar in record["bars"]:
            yield(bar["id"],midi.read_midifile(StringIO.StringIO(bar["data"])))
        for track in record["bars"]:
            yield(track["id"],midi.read_midifile(StringIO.StringIO(track["data"])))
        for bar_track in record["bars_tracks"]:
            yield(bar_track["id"],midi.read_midifile(StringIO.StringIO(bar_track["data"])))

def id_bartrack_itter(db):
    for record in db["records"]:
        record = db["records"][record]
        for bar_track in record["bars_tracks"]:
            yield(bar_track["id"],midi.read_midifile(StringIO.StringIO(bar_track["data"])))

def id_bar_itter(db):
    for record in db["records"]:
        record = db["records"][record]
        for track in record["bars"]:
            yield(track["id"],midi.read_midifile(StringIO.StringIO(track["data"])))

def id_track_itter(db):
    for record in db["records"]:
        record = db["records"][record]
        for track in record["bars"]:
            yield(track["id"],midi.read_midifile(StringIO.StringIO(track["data"])))

class MidiDB:
    def __init__(self, filename="midi.shelve"):
        self.shelve_db = shelve.open(filename)

    def get_pattern_by_id(self, passed_id):
        for pattern_id, record in id_pattern_itter(self.shelve_db):
            if pattern_id == passed_id:
                return record
        return None

    def itter_id_pattern(self):
        return id_pattern_itter(self.shelve_db)

    def itter_id_bartrack(self):
        return id_bartrack_itter(self.shelve_db)

    def itter_id_bar(self):
        return id_bar_itter(self.shelve_db)

    def itter_id_track(self):
        return id_track_itter(self.shelve_db)


def main():
    shelve_midi_db = shelve.open("midi.shelve", "w")
    records = {}
    filenames = get_midi_filenames(".")

    for index,filename in enumerate(filenames):
        title = "("+str(index)+"/"+str(len(filenames))+") " + filename
        print title
        print "="*len(title)
        record = create_record(filename)
        records[record["id"]] = record

    shelve_midi_db["records"] = records

    shelve_midi_db.close()



if __name__ == "__main__":
    main()