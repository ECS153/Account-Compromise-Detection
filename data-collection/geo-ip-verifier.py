########################################################################
# Testing the integrity of Azure geodata
#   - Before, we've experienced inconsistency in Azure geodata accuracy
########################################################################


import json
import mmdb_lookup


# 1. get IPs and locations from Azure

class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


ipList = []

azureLogs = []
iptoolLogs = []

with open('geoip-tester.json') as f:
    data = json.load(f)

i = 0
for login in data[0]['context']:
    if (login['lat'] is not None or login['lng'] is not None):
        ipList.append(login['ip'])
        loc = Location(login['lat'], login['lng'])
        print("IP:" + ipList[i] + "\tLAT:" + str(loc.lat) + "\tLON:" + str(loc.lng))
        azureLogs.append(loc)
        i += 1

# 2. Get location information from mmdb_lookup

i = 0
for ip in ipList:
    args = mmdb_lookup.getdata_mmdb(ip)
    loc = Location(args[0], args[1])
    print("IP:" + ipList[i] + "\tLAT:" + str(loc.lat) + "\tLON:" + str(loc.lng))
    iptoolLogs.append(loc)
    i += 1

# 3. Compare the location to see
i = 0
for log in azureLogs:
    azureLogs[i].lat = float("{:.2f}".format(log.lat))
    azureLogs[i].lng = float("{:.2f}".format(log.lng))
    print("LAT:" + str(loc.lat) + "\tLON:" + str(loc.lng))
    i += 1

i = 0
for log in iptoolLogs:
    iptoolLogs[i].lat = float("{:.2f}".format(log.lat))
    iptoolLogs[i].lng = float("{:.2f}".format(log.lng))
    print("LAT:" + str(loc.lat) + "\tLON:" + str(loc.lng))
    i += 1

# 4. Print Statistics of accuracy

n = 0
totCorrect = 0

for i in range(len(ipList)):
    n += 1
    tmp = [iptoolLogs, azureLogs]
    if (iptoolLogs[i] is azureLogs[i]):
        totCorrect += 1

print("\n\n\n")
# print("TOTAL: " + str(n) + "\tNUM CORRECT: " + str(totCorrect) + "\t% CORRECT: " + str((float(totCorrect) / float(n))))


azTotLAT = 0
azTotLON = 0

ipToolTotLAT = 0
ipToolTotLON = 0

for i in range(len(ipList)):
    azTotLAT += azureLogs[i].lat
    azTotLON += azureLogs[i].lng

    ipToolTotLAT += iptoolLogs[i].lat
    ipToolTotLON += iptoolLogs[i].lng

print("AZURE_LAT: " + str(azTotLAT) + "\tIP_LAT: " + str(ipToolTotLAT))
print("AZURE_LON: " + str(azTotLON) + "\tIP_LON: " + str(ipToolTotLON))

# 5. Save the lists to perform data analysis on
data = {}
data['ipList'] = ipList
data['AzureLocs'] = azureLogs
data['IpToolLocs'] = iptoolLogs
json_data = json.dumps(data)

print("\nWriting to IP_ANALYSIS.json!")
with open('IP_ANALYSIS.json', 'w+') as outfile:
    json.dump(data, outfile, indent=4)
