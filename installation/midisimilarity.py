#/usr/bin/env python
import editdistance
import midiutil
import mididb
import itertools


def track_timing_similarity(track_a, track_b):
    note_list1 = midiutil.track_to_note_list(track_a)
    note_list2 = midiutil.track_to_note_list(track_b)
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


def main():
    db = mididb.MidiDB()
    id_bartrack = list(db.itter_id_bartrack())
    #id_bartrack = itertools.islice(db.itter_id_bartrack(), 0, 5)

    bartracks = {}
    for bt_id, bartrack in id_bartrack:
        bartracks[bt_id] = bartrack

    #test = itertools.islice(db.itter_id_bartrack(), 0, 5)
    timing_similarities = {}
    count = 0
    for a,b in itertools.combinations(bartracks, 2):
        similarity = pattern_timing_similarity(bartracks[a], bartracks[b])
        print count, a,b, similarity
        count += 1

        if a not in timing_similarities:
            timing_similarities[a] = {}

        timing_similarities[a][b] = similarity

        if b not in timing_similarities:
            timing_similarities[b] = {}
        timing_similarities[b][a] = similarity


    db.shelve_db["bartrack_pattern_timing_similarity"] = timing_similarities
    db.shelve_db.close()
    #for pid, pattern in db.itter_id_pattern():
    #    print pid


if __name__ == '__main__':
    main()

