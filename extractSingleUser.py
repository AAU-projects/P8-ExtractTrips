import json
import gmplot
import os
import random
import collections

# FIX FOR MISSING MARKERS
# 1. Open gmplot.py in Lib/site-packages/gmplot
# 2. Replace line 29 (self.coloricon.....) with the following two lines:
#         self.coloricon = os.path.join(os.path.dirname(__file__), 'markers/%s.png')
#         self.coloricon = self.coloricon.replace('/', '\\').replace('\\', '\\\\')


def create_map(triplist_json):
    nice_colors = collections.deque(['#006699', '#6e4673', '#649e0b', '#f6921e', '#d14343', '#00afaf', '#66bbed', '#95609c', '#a1c964', '#faaf40', '#e56f6f', '#46dbdb'])

    start_set = False
    gmap = None
    # Go through selected trips.
    for trip in triplist_json:
        latt_list = []
        long_list = []

        transport = int(trip['Transport'])

        if transport == 0:  # WALK
            map_marker = '#000000'
        elif transport == 1:  # BIKE
            map_marker = '#0000FF'
        elif transport == 2:  # CAR
            map_marker = '#0000CD'
        else:  # TRANSIT
            map_marker = '#00BFFF'

        # Go through logs in a trip.
        for pos in trip['TripPositions']:
            latt_list.append(float(pos['Latitude']))
            long_list.append(float(pos['Longitude']))

        # Set the start of the map at the first trip.
        if not start_set:
            gmap = gmplot.GoogleMapPlotter(latt_list[0], long_list[0], 13)
            gmap.apikey = 'AIzaSyDPVbZkJPURllC7bFlR44iZhoLfwNSS5JI'
            start_set = True

        for pos in trip['TripPositions']:
            gmap.marker(float(pos['Latitude']), float(pos['Longitude']), color=map_marker, title=f"SPEED: {pos['Speed']}")

        color = None
        if nice_colors.count == 0:
            color = "#%06x" % random.randint(0, 0xFFFFFF)
        else:
            color = nice_colors[0]
            nice_colors.popleft()
        gmap.plot(latt_list, long_list, color, edge_width=5)

    gmap.draw(os.path.join(os.getcwd(), 'plots', f'resultTrips.html'))


def generate_map():
    with open('rawTrips.json') as file:
        trips_data = json.load(file)

    create_map(trips_data)
    print('\nMap created in plots/resultTrips.html')


if __name__ == '__main__':
    generate_map()
