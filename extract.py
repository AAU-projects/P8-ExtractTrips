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


def create_range_map(user_json, date, start, end):
    nice_colors = collections.deque(['#006699', '#6e4673', '#649e0b', '#f6921e', '#d14343', '#00afaf', '#66bbed', '#95609c', '#a1c964', '#faaf40', '#e56f6f', '#46dbdb'])

    start_set = False
    gmap = None
    # Go through selected trips.
    for i in range(start, end + 1):
        latt_list = []
        long_list = []
        # Go through logs in a trip.
        for log in user_json['TripDocuments'][date]['TripList'][i]['TripPositions']:
            latt_list.append(float(log['Latitude']['$numberDouble']))
            long_list.append(float(log['Longitude']['$numberDouble']))

        # Set the start of the map at the first trip.
        if not start_set:
            gmap = gmplot.GoogleMapPlotter(latt_list[0], long_list[0], 13)
            gmap.apikey = 'API KEY HERE PLEASE'
            start_set = True

        color = None
        if nice_colors.count == 0:
            color = "#%06x" % random.randint(0, 0xFFFFFF)
        else:
            color = nice_colors[0]
            nice_colors.popleft()
        gmap.plot(latt_list, long_list, color, edge_width=5)
        gmap.marker(latt_list[0], long_list[0], '#4682B4', title=f'TRIP: {str(i)}')
        gmap.marker(latt_list[-1], long_list[-1], '#B22222', title=f'TRIP: {str(i)}')

    gmap.draw(os.path.join(os.getcwd(), 'plots', f'result.html'))


def generate_map_gui():
    # Load JSON.
    collections = open('raw.json', 'r').readlines()
    users = []
    for user in collections:
        users.append(json.loads(user))

    # Select user.
    print('\nShowing users:')
    for idx, user in enumerate(users):
        print(f"[{idx}]: {user['_id']}")

    user_select = int(input('Please select a user: '))
    while user_select > len(users) - 1:
        print('Wrong input!')
        user_select = int(input('Please select a user: '))

    # Show trip date overview.
    print(f"\nShowing dates for user: {users[user_select]['_id']}")
    for idx, date in enumerate(users[user_select]['TripDocuments']):
        print(f"[{idx}]: {date['_id']}")

    # Select date.
    date_select = int(input('Please select a date: '))
    while date_select > len(users[user_select]['TripDocuments']) - 1:
        print('Wrong input!')
        date_select = int(input('Please select a date: '))

    # Show trip overview for chosen date.
    print(f"\nShowing trips for date: {users[user_select]['TripDocuments'][date_select]['_id']}")
    for idx, trip in enumerate(users[user_select]['TripDocuments'][date_select]['TripList']):
        print(f"[{idx}]: {trip['_id']}")

    # Range select
    print('\nPlease select a range of trips to map. Give the same number twice to only map one.')
    start_range = int(input('Start range: '))
    end_range = int(input('End range: '))

    create_range_map(users[user_select], date_select, start_range, end_range)
    print('\nMap created in plots/result.html')


if __name__ == '__main__':
    generate_map_gui()
