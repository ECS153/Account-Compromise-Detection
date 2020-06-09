############################################
# MaxMind GeoIP API Script
#   - Draws geodata from MaxMind databases
############################################


import json, sys, re
import requests
import getopt, socket
import geoip2.database
import geoip2.webservice

cred_json = open('../maxmind_creds.json', )
creds = json.load(cred_json)

MMACCT = int(creds[0]['MMACCT'])
MMLKEY = creds[0]['MMLKEY']

# Maxmind local databases
# MOST RECENTLY UPDATED 5/19/2020
MMASNDB = '../databases/GeoLite2-ASN.mmdb'
MMCITYDB = '../databases/GeoLite2-City.mmdb'


def mmInitWeb(mmWebAccount=MMACCT, mmWebKey=MMLKEY):
    webReader = geoip2.webservice.Client(mmWebAccount, mmWebKey)

    try:
        myIP = webReader.city()
        print('Remaining MaxMind web queries for account #' + str(mmWebAccount) + ' = ' + str(
            myIP.maxmind.queries_remaining))
    except geoip2.webservice.AuthenticationError as err:
        print('[WARN] ' + str(err) + '. IP insight info will be unavailable')
    except geoip2.webservice.InvalidRequestError as err:
        print('[WARN] During web service initialization. ' + str(err))
    except geoip2.webservice.OutOfQueriesError as err:
        print('[WARN] ' + str(err) + '. IP insight info will be unavailable')

    return webReader


def mmInitDB(mmASNFile=MMASNDB, mmCityFile=MMCITYDB):
    (asnReader, cityReader) = (None, None)

    try:
        asnReader = geoip2.database.Reader(mmASNFile)
    except (IOError, FileNotFoundError):
        print('[WARN] No MaxMind database file ' + mmASNFile + '. ASN information will be unavailable.')
    except geoip2.database.maxminddb.errors.InvalidDatabaseError as err:
        print('[WARN] ' + str(err) + '. ASN information will be unavailable.')

    try:
        cityReader = geoip2.database.Reader(mmCityFile)
    except (IOError, FileNotFoundError):
        print(
            '[WARN] No MaxMind database file ' + mmCityFile + '. Country/City information will be unavailable.')
    except geoip2.database.maxminddb.errors.InvalidDatabaseError as err:
        print(str(err) + '. Country/City information will be unavailable.')

    return asnReader, cityReader


def mmDBInfo(ipaddr, asnReader=None, cityReader=None):
    ipinfo = {}

    # get geo info
    try:
        response = cityReader.city(ipaddr)
        ipinfo['city'] = response.city.name
        ipinfo['country'] = response.country.name
        ipinfo['location'] = {
            'latitude': response.location.latitude,
            'longitude': response.location.longitude
        }
        ipinfo['trait'] = {
            'is_anon': response.traits.is_anonymous,
            'is_anon_vpn': response.traits.is_anonymous_vpn,
            'is_hosting': response.traits.is_hosting_provider,
            'is_tor': response.traits.is_tor_exit_node,
            'user_type': response.traits.user_type
        }
    except:
        print('mmDBInfo: [WARN] Unable to get geoIP info.')

    ipinfo['IPAddress'] = ipaddr

    return ipinfo


def mmWebInfo(ipaddr, webReader=None):
    ipinfo = {}
    # get insight data
    try:
        response = webReader.insights(ipaddr)
        ipinfo['city'] = response.city.name
        ipinfo['country'] = response.country.name
        ipinfo['location'] = {
            'latitude': response.location.latitude,
            'longitude': response.location.longitude
        }

    except:
        print('mmWebInfo: [WARN] Unable to get IP insight data from web.')

    ipinfo['IPAddress'] = ipaddr

    return ipinfo

def full_response(ipaddr, asnReader=None, cityReader=None):
    # get geo info
    try:
        response = cityReader.city(ipaddr)
    except:
        print('mmDBInfo: [WARN] Unable to get geoIP info.')


    return response


def getLatLng(ipinfo):
    lat = ipinfo['location']['latitude']
    lng = ipinfo['location']['longitude']
    args = [lat, lng]
    return args


def getdata_web(ip):
    webReader = mmInitWeb()
    extInfo = mmWebInfo(ip, webReader)
    return getLatLng(extInfo)


def getdata_mmdb(ip):
    (asnReader, cityReader) = mmInitDB()
    extInfo = mmDBInfo(ip, asnReader, cityReader)
    return getLatLng(extInfo)


def get_full_object(ip):
    (asnReader, cityReader) = mmInitDB()
    full_object = mmDBInfo(ip, asnReader, cityReader)
    return full_object
