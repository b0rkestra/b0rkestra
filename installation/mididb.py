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
import midiremap


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


def create_record(filename, include_data = False):
    print "Creating record", filename
    record = {}
    record["id"] = generate_id(open(filename, "rb"))
    record["filename"] = filename

    try:
        pattern = midi.read_midifile(filename)
    except:
        print "Error"
        return None
    
    if include_data:
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


def populate_shelve_db(db_filename="metamidi.shelve", directory="./midi-sample", include_data=False):
    shelve_midi_db = shelve.open(db_filename, "c", writeback=True)

    for index,filename in enumerate(filenames):
        title = "("+str(index)+"/"+str(len(filenames))+") " + filename
        print title
        print "="*len(title)
        record = create_record(filename, include_data)
        if record != None:
            shelve_midi_db[record["id"]] = record
            #shelve_midi_db.sync()

    shelve_midi_db.close()    



def create_json_filename_file(output_filename="filenames.json", directory="./midi"):
    filenames = get_midi_filenames(directory)
    filenames = json.dumps(filenames)
    f = open(output_filename, "w")
    f.write(filenames)
    return filenames



class MidiDB:
    def __init__(self, filename="metamidi.shelve"):
        self.shelve_db = shelve.open(filename)
        self.keys = self.shelve_db.keys()
        self.__key_index__ = {}
        self.__scale_index__= {}
        self.__key_scale_index__= {}

        #populate key & scale indexs
        for uid in self.keys:
            record = self.shelve_db[uid]
            if record["key"] in self.__key_index__:
                self.__key_index__[record["key"]].append(record["id"])
            else:
                self.__key_index__[record["key"]] = [record["id"]]

            for scale in record["scale"]:
                if scale in self.__scale_index__:
                    self.__scale_index__[scale].append(record["id"])
                else:
                    self.__scale_index__[scale] = [record["id"]]

                if (record["key"], scale) in self.__key_scale_index__:
                    self.__key_scale_index__[(record["key"], scale)].append(record["id"])
                else:
                    self.__key_scale_index__[(record["key"], scale)] = [record["id"]]

    def record(self, passed_id):
        pattern = None
        try:
            record = self.shelve_db[passed_id]
        except KeyError:
            pass
        return record

    def random_record(self):
        uid = random.choice(self.keys)
        return self.shelve_db[uid]

    def random_pattern(self):
        record = self.random_record()
        print record["id"]
        pattern = midi.read_midifile(record["filename"])
        return pattern

    def pattern(self, passed_id):
        record = self.record(passed_id)
        pattern = None
        if record != None: pattern = midi.read_midifile(record["filename"])
        return pattern


    def records_in_key(self, key):
        if not key in self.__key_index__:
            return []
        records = []
        for uid in self.__key_index__[key]:
            records.append(self.shelve_db[uid])
        return records


    def records_in_scale(self, scale):
        records = []
        if not scale in self.__scale_index__:
            return records
        for uid in self.__scale_index__[scale]:
            records.append(self.shelve_db[uid])
        return records


    def records_in_key_and_scale(self, key, scale):
        records = []
        if not (key, scale) in self.__key_scale_index__:
            return records
        for uid in self.__key_scale_index__[(key, scale)]:
            records.append(self.shelve_db[uid])
        return records



def main():
    db = MidiDB();


    records = db.records_in_key("C")

    result_pattern = midi.Pattern(resolution=480) 

    songs = []
    for i in range(5):
        uid = random.choice(records)["id"];
        pattern = db.pattern(uid)
        midiutil.pattern_to_resolution(pattern, 480)

        track = random.choice(pattern)
        result_pattern.append(track)


        songs.append(pattern)

    remapper = midiremap.MidiRemapper("b0rkestra_description.json", result_pattern)
    remapper.remap_pattern(result_pattern)


    midi.write_midifile("test.mid", result_pattern)


    #print db.get_record(db.keys[10]);
    #for key in db.__key_index__:
    #    print key, len(db.__key_index__[key])
    #for scale in db.__scale_index__:
    #    print scale, len(db.__scale_index__[scale])
    #print len(db.get_records_in_key('A'))



if __name__ == "__main__":
    main()