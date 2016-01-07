import hashlib
import midi
import midisanitize
import midiutil
import StringIO

def generate_id(f):
    hash = hashlib.md5()
    #with open(fname, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
        hash.update(chunk)
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

    record["split_bars"] = []
    print "### Splitting to Bars"
    for bar in range(record["max_tick"]/record["ticks_per_bar"]):
        bar_pattern = midiutil.get_bar_from_pattern(pattern, bar)
        bar_id = generate_id(midiutil.midi_to_file_object(bar_pattern))
        bar = {"name": str(bar), "id":bar_id, "data":midiutil.midi_to_data(bar_pattern)}
        record["split_bars"].append(bar)
    
    record["split_tracks"] = []
    tracks = midiutil.split_tracks_to_patterns(pattern)
    print tracks
    for index, name in enumerate(record["track_names"]):
        track_pattern = tracks[index]
        track_id = generate_id(midiutil.midi_to_file_object(track_pattern))
        track = {"name": name, "data":midiutil.midi_to_data(track_pattern)}
        record["split_tracks"].append(track)
    return record


def main():
    create_record("decoy.mid")


if __name__ == "__main__":
    main()