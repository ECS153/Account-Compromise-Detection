##########################################################
# Script to analyze Microsoft Azure GeoIP data accuracy
# TODO: WIP
##########################################################

import json
#import iptools


# 1.

class Location:
  def __init__(self, lat, lng):
    self.lat = lat
    self.lng = lng

azureLocs = []
iptoolLocs = []

ipList = []

with open('geoip-tester.json') as f:
  data = json.load(f)

for login in data[0]['context']:
    ipList.append(login['ip'])
    azureLocs.append(Location(login['lat'], login['lng']))






