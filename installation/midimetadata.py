#!/usr/bin/env python
import numpy
from nltk.cluster import KMeansClusterer, GAAClusterer, euclidean_distance
import nltk.corpus
import nltk.stem
import os
import midi
import midiutil
stemmer_func = nltk.stem.snowball.SnowballStemmer("english").stem
stopwords = set(nltk.corpus.stopwords.words('english'))

def normalize_word(word):
    return stemmer_func(word.lower())


def get_words(titles):
    words = set()
    for title in titles:
        for word in title.split():
            words.add(normalize_word(word))
    return list(words)


def vectorspaced(title, words):
    title_components = [normalize_word(word) for word in title.split()]
    return numpy.array([word in title_components and not word in stopwords for word in words], numpy.short)


def get_tracknames():
    filenames = []
    count = 0
    for root, subFolders, files in os.walk('.'):
        count +=1
        if count == 9:
            break
        files = [os.path.join(root, filename) for filename in files if filename.lower().endswith(".mid")]
        filenames += files

    filenames = filenames[:100]
    tracknames = []
    for filename in filenames:
        print "processing", filename
        try:
            pattern = midi.read_midifile(filename)
            current_tracknames = midiutil.get_track_names(pattern)
            current_tracknames =  [trackname.rstrip().lstrip().lower().encode('ascii', 'ignore') for trackname in current_tracknames]
            #current_tracknames = [trackname for trackname in tracknames if trackname != ""]
            tracknames += current_tracknames 
        except:
            print "    bad file", filename
    tracknames = [' '.join(ch for ch in t if ch.isalnum()) for t in tracknames if t != '']
    print tracknames
    return tracknames


def main():
    tracknames = get_tracknames()  
    #title_file = open("example_jobs.txt", 'r')

    #job_titles = [line.strip() for line in title_file.readlines()]
    words = get_words(tracknames)

    cluster = KMeansClusterer(20, euclidean_distance, avoid_empty_clusters=True)
    cluster.cluster([vectorspaced(trakname, words) for trakname in tracknames if trakname])
    classified_examples = [cluster.classify(vectorspaced(trackname, words)) for trackname in tracknames]


    for cluster_id, title in sorted(zip(classified_examples, tracknames)):
        print cluster_id, title


if __name__ == '__main__':
    main()