###########################################################################################
# MaxMind DB Query Tool
# Currently, we query via webclient
# In the future, to support much larger data volumes, we will use local .mmdb databases
###########################################################################################

import json
import geoip2.database
import geoip2.webservice

# Default name of the MaxMind database files for the DB lookup option
MMASNDB = './GeoLite2-ASN.mmdb'
MMCITYDB = './GeoLite2-City.mmdb'

# Get creds for MaxMind
cred_json = open('maxmind_creds.json', )
creds = json.load(cred_json)

MMACCT = int(creds[0]['MMACCT'])
MMLKEY = creds[0]['MMLKEY']


def mmInitWeb(mmWebAccount=MMACCT, mmWebKey=MMLKEY):
    webReader = geoip2.webservice.Client(mmWebAccount, mmWebKey)
    return webReader


# Initializes local database
# Will switch to this method once we retrieve a local copy of the .mmdb's
def mmInitDB(mmASNFile=MMASNDB, mmCityFile=MMCITYDB):
    (asnReader, cityReader) = (None, None)

    try:
        asnReader = geoip2.database.Reader(mmASNFile)
    except (IOError, FileNotFoundError):
        print('ERROR: No MaxMind database file ' + mmASNFile + '. ASN information will be unavailable.')
    except geoip2.database.maxminddb.errors.InvalidDatabaseError as err:
        print('ERROR: ' + str(err) + '. ASN information will be unavailable.')

    try:
        cityReader = geoip2.database.Reader(mmCityFile)
    except (IOError, FileNotFoundError):
        print(
            'ERROR: No MaxMind database file ' + mmCityFile + '. Country/City information will be unavailable.')
    except geoip2.database.maxminddb.errors.InvalidDatabaseError as err:
        print('ERROR: ' + str(err) + '. Country/City information will be unavailable.')

    return asnReader, cityReader


def mmWebInfo(ip, webReader=None):
    data = {}
    data['IPAddress'] = ip
    try:
        response = webReader.insights(ip)
        data['city'] = response.city.name
        data['country'] = response.country.name
        data['location'] = {
            'latitude': response.location.latitude,
            'longitude': response.location.longitude
        }

    except:
        print('WEBCLIENT WARNING: Unable to get IP insight data from web.')

    return data


def getLatLng(data):
    lat = data['location']['latitude']
    lng = data['location']['longitude']
    return lat, lng


def getData(ip):
    # Initialize web client
    # When we get the local mmdb's, we can switch to mmInitDB
    webReader = mmInitWeb()
    extInfo = mmWebInfo(ip, webReader)

    lat, lng = getLatLng(extInfo)

    return lat, lng

# lat, lng = getData("204.11.56.48")
# print(str(lat) + " " + str(lng))


# to use, call getData from this script and provide IP address (as string) as the argument
