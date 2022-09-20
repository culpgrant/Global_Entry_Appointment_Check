test = [{'locationId': 5004, 'startTimestamp': '2022-09-22T08:15', 'endTimestamp': '2022-09-22T08:30', 'active': True, 'duration': 15, 'remoteInd': False},{'locationId': 1004, 'startTimestamp': '2022-09-22T08:15', 'endTimestamp': '2022-09-22T08:30', 'active': True, 'duration': 15, 'remoteInd': False}]
locations = {5004: 'Test location', 1004: 'testlocation 2'}


list_location_names = []
# Create the list of location names
for loc in test:
    # Map the Id to the location name
    name = locations[loc['locationId']]
    list_location_names.append(name)

print(' and '.join(list_location_names))