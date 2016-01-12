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
import mididb

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
#     bars:[
#         {"id":"MD5hash_of_data", "data":binary_bar_data, "name":"bar_number"}
#     ],
#     tracks:[
#         {"id":"MD5hash_of_data", "data":binary_track_data, "name":"track_name"}
#     ],
#     bars_tracks:[
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
    db = mididb.MidiDB()
    for key in db.shelve_db["bartrack_pattern_timing_similarity"]:
        print key
        pattern = db.get_pattern_by_id(key)
        midi.write_midifile(key+".mid", pattern)




if __name__ == "__main__":
    main()