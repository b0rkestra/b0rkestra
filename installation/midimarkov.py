#!/usr/bin/env python

import midi
import midiutil
import mididb
import random
from itertools import tee, izip

def nwise(iterable, n=2):
    group = tee(iterable,n)
    for i,it in enumerate(group):
        for a in range(i):
            next(it, None)
    return izip(*group)


class MarkovModel:
    def __init__(self, ngram_size = 2):
        self.ngram_size = ngram_size
        self.model = {}

    def bulk_add(self, data):
        for datums in nwise(data, self.ngram_size+1):
            ngram = tuple(datums[:-1])
            next_state = datums[-1]
            self.add(ngram, next_state)

    def add(self, ngram, next_state):
        if len(ngram) != self.ngram_size:
            raise IndexError("ngram must be of size "+str(self.ngram_size))
        if not ngram in self.model:
            self.model[ngram] = {next_state:1}
        else:
            if not next_state in self.model[ngram]:
                self.model[ngram][next_state] = 1
            else:
                self.model[ngram][next_state] += 1

    def weighted_random_nexstate(self, state):

        next_states = self.model[state]
        next_states = list(next_states.items())
        return self.__weighted_choice__( next_states)


    def __weighted_choice__(self, choices):
        total = sum(w for c, w in choices)
        r = random.uniform(0, total)
        upto = 0
        if r > 1:
            print "rand"
        else:
            print "boo"
        for c, w in choices:
           if upto + w >= r:
              return c
           upto += w
        assert False, "Shouldn't get here"


def main():

    markov = MarkovModel(ngram_size=10)
    filenames = mididb.get_midi_filenames(".")


    for index,filename in enumerate(filenames):
        title = "("+str(index)+"/"+str(len(filenames))+") " + filename
        #print title
        #print "="*len(title)
        pattern = midi.read_midifile(filename)
        time_sigs = midiutil.get_events_from_pattern(pattern, "Time Signature")
        for time_sig in time_sigs:
            if time_sig.denominator !=4 and time_sig.numerator !=4:
                print time_sig.denominator, time_sig.numerator
            if pattern.resolution != 240:
                print pattern.resolution, filename 
            #print time_sig.denominator, time_sig.numerator


    #     for track in pattern:
    #         markov.bulk_add(track)


    # output = list(random.choice(markov.model.keys()))

    # for a in range(200):
    #     next_state = markov.weighted_random_nexstate( tuple(output[-(markov.ngram_size):]) )
    #     output.append(next_state)

    # pattern = midi.Pattern()
    # track = midi.Track()
    # for event in output:
    #     track.append(event)

    # pattern.append(track)
    # midi.write_midifile("output.mid", pattern)



    # a.sort()
    # print a[3] == a[5]

    # for note, in a:
    #     try:
    #         print note.tick, note.channel, note.pitch
    #     except:
    #         print "--"





if __name__ == '__main__':
    main()