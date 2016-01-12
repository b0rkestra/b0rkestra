#!/usr/bin/env python

import midi
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


def main():
    pattern = midi.read_midifile("./midi/drum_patterns.mid")
    
    markov = MarkovModel(ngram_size=2)
    for track in pattern:
        markov.bulk_add(track)
    
    a = markov.model
    print a

    # a.sort()
    # print a[3] == a[5]

    # for note, in a:
    #     try:
    #         print note.tick, note.channel, note.pitch
    #     except:
    #         print "--"





if __name__ == '__main__':
    main()