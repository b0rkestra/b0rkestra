#!/usr/bin/env python
import json
import midi
import midiutil
import mididb
import random
import operator



def __get_track_channel__(track):
	channels = {}
	for event in midiutil.get_events_from_track(track, "Note On"):
		if event.channel in channels:
			channels[event.channel] += 1
		else:
			channels[event.channel] = 1
	if len(channels) == 0:
		return None
	main_channel = sorted(channels.items(), key=operator.itemgetter(1))[-1][0]
	return main_channel


def __create_range_mapping_for_track__(track, target_channel, lower_note=None, upper_note=None):
	mapping = {}
	for event in midiutil.get_events_from_track(track, "Note On"):
		key = (event.channel, event.pitch)
		
		channel = target_channel
		pitch = event.pitch

		if lower_note != None:
			while pitch < lower_note:
				pitch += 12
		if upper_note != None:
			while pitch > upper_note:
				pitch -= 12
		value = (channel, pitch)
		mapping[key] = value
	return mapping


def __check_track_for_direct_mapping__(track, description):
	mapping = {}
	channel = __get_track_channel__(track)
	if channel == None: return None

	for instrument in description["instruments"]:
		try:
			if description["instruments"][instrument]["input_channel"] == channel:
				range_min = description["instruments"][instrument].get("range_min")
				range_max = description["instruments"][instrument].get("range_max")
				return __create_range_mapping_for_track__(track, channel, range_min, range_max)
		except KeyError:
			pass
	if len(mapping) == 0:
		return None


def __find_best_fitting_instrument_for_track(track, description):
	fit = {}
	for instrument in description["instruments"]:
		#if there's an explcit mapping for this instrument then ignore the instrument.
		#instrument = description["instruments"][instrument]
		if description["instruments"][instrument].get("input_channel"): continue

		miss = 0
		for event in midiutil.get_events_from_track(track, "Note On"):
			if description["instruments"][instrument].get("range_min"):
				if event.pitch < description["instruments"][instrument]["range_min"]:
					miss += 1
			if description["instruments"][instrument].get("range_max"):
				if event.pitch > description["instruments"][instrument]["range_max"]:
					miss += 1
		fit[instrument] = miss
	
	best_instrument = description["instruments"][sorted(fit.items(), key=operator.itemgetter(1))[0][0]]
	return best_instrument






def __build_mapping__(description, pattern):
	mapping = {}
	for track in pattern:
		#check if theres a direct mapping for the tracks midi channel
		track_mapping = __check_track_for_direct_mapping__(track, description)
		if track_mapping:
			mapping.update(track_mapping)
			continue

		#otherwise find the closest fitting midi instrument for the track & create a mapping
		instrument = __find_best_fitting_instrument_for_track(track, description)
		track_mapping = __create_range_mapping_for_track__(track, instrument["output_channel"], instrument.get("range_min"), instrument.get("range_max"))
		mapping.update(track_mapping)

	return mapping



class MidiRemapper:
	def __init__(self, description_filename, pattern):
		self.description = json.load(open(description_filename))
		self.mappings = __build_mapping__(self.description, pattern)
		#print self.mappings

	def remap(self, event):
		if event.name != "Note On" and event.name != "Note Off":
			return event
		remap = self.mappings[(event.channel, event.pitch)]
		event.channel = remap[0]
		event.pitch = remap[1]
		return event

	def remap_pattern(self, pattern):
		for track in pattern:
			for event in track:
				event = self.remap(event) 
		return pattern


def main():
	filenames = mididb.get_midi_filenames("./midi-sample")
	filename = random.choice(filenames)
	#pattern = midi.read_midifile("./midi-sample/Claude_von_Stroke_-_Whos_Afraid_Of_Detroit__John_20071211160037.mid")
	pattern = midi.read_midifile(filename)
	remapper = MidiRemapper("b0rkestra_description.json", pattern)


if __name__ == '__main__':
	main()