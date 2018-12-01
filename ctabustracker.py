import urllib.request
import sys
from xml.etree.ElementTree import parse
import webbrowser
import time

dave_lattitude = 41.980262
dave_longitude = -87.668452

# get the data from the web and put it in a file
def make_xml(filename):
    u = urllib.request.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
    data = u.read()
    f = open(filename, 'wb')
    f.write(data)
    f.close()

# this takes an xml file and pulls out relevant interested tree branches
def parse_xml(file):
    doc = parse(file)
    parsed_lst = []
    for bus in doc.findall('bus'):
        bus_id = bus.findtext('id')
        direction = bus.findtext('d')
        lattitude = bus.findtext('lat')
        bus_stats_lst =[bus_id, direction, lattitude]
        parsed_lst.append(bus_stats_lst)
    return parsed_lst

# calculates a rough distance between two latitudes
def distance(lat1, lat2):
    distance = 69*(lat1 - lat2)
    return distance

# pulls a fresh xml file, compares it to a previously identified group, and prints updated data for that group
def monitor(likelies):
    likelies_id = []
    for likely in likelies:
        likelies_id.append(likely[0])
    u = urllib.request.urlopen('http://ctabustracker.com/bustime/map/getBusesForRoute.jsp?route=22')
    doc = parse(u)
    for bus in doc.findall('bus'):
        bus_id = bus.findtext('id')
        if bus_id in likelies_id:
            lat = bus.findtext('lat')
            direct = bus.findtext('d')
            dist = distance(float(lat), dave_lattitude)
            print(bus_id, direct, lat, dist, 'miles away')
    print('-'*10)

# runs the appropriate xml parsing, picks a group, and sets up periodic monitoring via xml refresh 
def main():
    filename = 'rt22.xml'
    make_xml(filename)
    bus_stats_lst = parse_xml(filename)
    likely_bus_lst = []
    for bus in bus_stats_lst:
        lattitude = float(bus[2])
        if 'North' in bus[1] and lattitude > dave_lattitude:
            likely_bus_lst.append(bus)
    for bus in likely_bus_lst:
        bus.append(distance(float(bus[2]),dave_lattitude))
    count = 0
    while True:
        monitor(likely_bus_lst)
        time.sleep(5)
        count +=1
        if count == 4:
            break

if __name__ == '__main__':
    main()
