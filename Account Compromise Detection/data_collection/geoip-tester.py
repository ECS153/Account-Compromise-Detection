#################################################################################################
# Script to acquire 1000 random sign-in logs
# This is an stripped version of our data-collection-script.py
# We will perform a statistical analysis to determine accuracy of Microsoft Azure GeoIP data
#      - We've previously experienced problems with Azure GeoIP data,
#        so we want to verify against a known accurate tool: MaxMind
#################################################################################################

import json
import logging

import requests
import msal

import pprint
import datetime
import os
import sys

config = json.load(open(sys.argv[1]))

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
)

result = None
result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    endpoint = config["endpoint"]

    # Calling graph using the access token
    graph_data = requests.get(
        endpoint,
        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
    print("Graph API call result: ")

    pp = pprint.PrettyPrinter(indent=4)

    today = datetime.datetime.now() - datetime.timedelta(hours=6)
    temp_split = str(today).split(" ")
    today = temp_split[0]
    # Format as per Graphs API 2014-01-01T00:00:00Z

    data_master = []

    endpoint = "https://graph.microsoft.com/beta/auditLogs/signIns?&$filter=createdDateTime ge " + today
    print(endpoint)

    graph_data = requests.get(
        endpoint,
        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
    print("Graph API sub-call: ")

    temp_count = 0
    data = {}
    data['context'] = []

    for item in graph_data['value']:
        ip = item['ipAddress']

        lat = item['location']['geoCoordinates']['latitude']
        lng = item['location']['geoCoordinates']['longitude']

        temp_count += 1

        data['context'].append({
            'ip': ip,
            'lat': lat,
            'lng': lng
        })

        # print(item['location'])

        # print(graph_data['value']['userDisplayName'])
        data['records_in_context'] = str(temp_count)
        # print(temp_count)

    data_master.append(data)

    print("\nWriting to geoip-tester.json!")
    with open('geoip-tester.json', 'w+') as outfile:
        json.dump(data_master, outfile, indent=4)

    print("TESTER END")


else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug