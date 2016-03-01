#!/usr/bin/env python
import hashlib
import random
import midi
import midisanitize
import midiutil
import StringIO
import shelve
import json
import copy
import base64
import os
import matplotlib.pyplot as plt

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
    print "Creating record", filename
    record = {}
    record["id"] = generate_id(open(filename, "rb"))
    record["filename"] = filename

    try:
        pattern = midi.read_midifile(filename)
    except TypeError:
        print "Error"
        return None

    record["data"] = midiutil.midi_to_data(pattern)
    record["time_signature"] = midiutil.get_time_signature(pattern)
    record["tempo"] = midiutil.get_tempo(pattern)
    record["track_names"] = midiutil.get_track_names(pattern)
    record["resolution"] = pattern.resolution
    record["note_distribution"] = midiutil.get_note_distribution(pattern,[9])
    record["key"] = midiutil.guess_key(pattern, record["note_distribution"])
    record["scale"] = midiutil.guess_scale(record["key"], record["note_distribution"])
    

    #for track in pattern:
    #    print midiutil.get_track_name(track)
    #    dist = midiutil.get_note_distribution(track, [], False)
    #    plt.bar(range(len(dist)), dist.values(), align="center")
    #    plt.xticks(range(len(dist)), dist.keys())
    #    plt.show()

    # dist = record["note_distribution"]
    

    return record


def record_to_json(record):
    record = copy.deepcopy(record)
    record["data"] = base64.b64encode(record["data"])
    return json.dumps(record)


def json_to_record(json_record):
    record = json.loads(json_record)
    record["data"] = base64.b64decode(record["data"])
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




class MidiDB:
    def __init__(self, filename="midi.shelve"):
        self.shelve_db = shelve.open(filename)

    def get_pattern_by_id(self, passed_id):
        for pattern_id, record in id_pattern_itter(self.shelve_db):
            if pattern_id == passed_id:
                return record
        return None


def main():

    filenames = get_midi_filenames("./midi-sample")
    
    #for filename in [random.choice(filenames)]:
    #    print create_record(filename)


    shelve_midi_db = shelve.open("midi.shelve", "c", writeback=True)

    for index,filename in enumerate(filenames):
        title = "("+str(index)+"/"+str(len(filenames))+") " + filename
        print title
        print "="*len(title)
        record = create_record(filename)
        if record != None:
            shelve_midi_db[record["id"]] = record
            #shelve_midi_db.sync()

    shelve_midi_db.close()



if __name__ == "__main__":
    main()