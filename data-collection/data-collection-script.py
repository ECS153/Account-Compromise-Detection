# Query Engine for Microsoft Azure with support for GeoIP tools
# Run with parameter parameters.json

import sys
import json
import logging

import requests
import msal

import datetime
import threading
import os
import sys

# import pprint
# pp = pprint.PrettyPrinter(indent=4)

# Testing query speed with free-license service
# Will fully convert to MaxMind after testing
# Thus, ip2geotools will be temporary
from ip2geotools.databases.noncommercial import DbIpCity

# Load in config file
# WILL NOT BE INCLUDED IN GITHUB. THIS FILE REMAINS ON THE MACHINE.
config = json.load(open(sys.argv[1]))

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    # token_cache=...  # Default cache is in memory only. SerializableTokenCache Documentation:
    # https://msal-python.rtfd.io/en/latest/#msal.SerializableTokenCache
)


def setQueryDate(daysIn):
    setDate = datetime.datetime.now() - datetime.timedelta(days=daysIn)

    # Format as per Graphs API 2014-01-01T00:00:00Z
    tempSplit = str(setDate).split(" ")

    # Optional logic to include time as well, which Graphs query doesn't like for some reason...
    # splitForDays= temp_split[1].split(".")

    # This returns properly formatted date WITHOUT hours
    setDate = tempSplit[0]

    return setDate


# Init result
result = None

# Look up a token from cache with no end user
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    # Sets endpoint
    # Our specified endpoint will query for the last 10 risky users,
    # ordered by when the risk level was most recently updated.
    endpoint = config["endpoint"]

    # Calling graph using the access token
    graph_data = requests.get(
        endpoint,
        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
    # print("Response: ")
    # print(json.dumps(graph_data, indent=2))

    # Collect unique Azure object id's for each risky user in our /beta/riskyUsers query
    riskyUsers_id = []
    counter = 0
    for each in graph_data['value']:
        if not counter == 10:
            riskyUsers_id.append(each['id'])
            counter += 1
        else:
            break

    # Call function to get date for time window (14 days currently)
    # Function will also format it to fit the Microsoft Graphs query
    setQueryDate_result = setQueryDate(14)

    data_master = []
    for each in riskyUsers_id:
        print("Risky user object id: " + each)

        endpoint = "https://graph.microsoft.com/beta/auditLogs/signIns?&$filter=userID eq '" + each + "' and createdDateTime ge " + setQueryDate_result

        graph_data = requests.get(
            endpoint,
            headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
        print("Sending request with endpoint: " + endpoint)

        logCount = 0
        data = {}
        data['id'] = each
        data['context'] = []

        # Get ip, lat, lng for each signIn event per specified riskyUser object id:
        for item in graph_data['value']:
            ip = item['ipAddress']
            lat = None
            lng = None

            # If location is unavailable, then make additional call to a GeoIP service
            # Azure/Graphs API returns None for IPv6 addresses
            # TODO: This logic would be changed to MaxMind when testing is complete
            if item['location']['city'] is None:
                response = DbIpCity.get(ip, api_key='free')
                lat = response.latitude
                lng = response.longitude
            else:
                lat = item['location']['geoCoordinates']['latitude']
                lng = item['location']['geoCoordinates']['longitude']

            createdDateTime = item['createdDateTime']
            logCount += 1

            data['context'].append({
                'ip': ip,
                'datetime': createdDateTime,
                'lat': lat,
                'lng': lng
            })

        data['records_in_context'] = str(logCount)

        data_master.append(data)

    # Write the data to the raw .json file
    # This .json is passed to algorithm script
    with open('data.json', 'w+') as outfile:
        # TODO: remove indentation to increase efficiency!
        json.dump(data_master, outfile, indent=4)

    print("data-collection-script.py has completed!")

# Get errors if Graphs API call fails...
else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))
