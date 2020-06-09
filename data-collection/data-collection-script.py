#################################################################################
# Main Data Collection Script
#   - Data comes from Microsoft Azure logs and MaxMind DB for contextual geodata
#################################################################################


import json
import logging

import requests
import msal

import pprint
import datetime
import sys

import mmdb_lookup


config = json.load(open(sys.argv[1]))

# Create a preferably long-lived app instance which maintains a token cache.
app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authority"],
    client_credential=config["secret"],
    )

result = None

# Get token from cache, if possible
result = app.acquire_token_silent(config["scope"], account=None)

# Otherwise, refer to json containing app secrets
if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

if "access_token" in result:
    # Specify query endpoint
    endpoint = "https://graph.microsoft.com/beta/riskyUsers?$filter=riskLevel eq 'high'&$orderby=riskLastUpdatedDateTime desc"

    # Calling graph using the access token
    graph_data = requests.get(
        endpoint,
        headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
    print("Graph API call result: ")

    # Query gets top 20 results, so load those into a riskUsers_id array
    riskyUsers_id = []
    counter = 0
    for each in graph_data['value']:
        if not counter == 20:
            riskyUsers_id.append(each['id'])
            counter += 1
        else:
            break

    # Date time parsing
    today = datetime.datetime.now() - datetime.timedelta(days=14)
    temp_split = str(today).split(" ")
    print(temp_split)
    temptemp = temp_split[1].split(".")
    print(temptemp)
    today = temp_split[0]
    # Format as per Graphs API 2014-01-01T00:00:00Z

    data_master = []
    for each in riskyUsers_id:
        print(each)

        # Specify new endpoint to get all user sign-ins from past 14 days
        endpoint = "https://graph.microsoft.com/beta/auditLogs/signIns?&$filter=userID eq '" + each + "' and createdDateTime ge " + today
        print(endpoint)

        graph_data = requests.get(
            endpoint,
            headers={'Authorization': 'Bearer ' + result['access_token']}, ).json()
        print("Graph API sub-call: ")

        temp_count = 0
        data = {}
        data['id'] = each
        data['context'] = []

        for item in graph_data['value']:
            ip = item['ipAddress']
            lat = None
            lng = None

            if item['location']['city'] is None:
                print("Pulling from MaxMind")
                response = mmdb_lookup.getdata_mmdb(ip)
                lat = response[0]
                lng = response[1]
                print(ip)
                print(response)
            else:
                lat = item['location']['geoCoordinates']['latitude']
                lng = item['location']['geoCoordinates']['longitude']

            createdDateTime = item['createdDateTime']
            temp_count += 1

            clientAppUsed = item['clientAppUsed']
            userAgent = item['userAgent']
            os = item['deviceDetail']['operatingSystem']
            browser = item['deviceDetail']['browser']

            details = {}
            details['clientAppUsed'] = clientAppUsed
            details['userAgent'] = userAgent
            details['os'] = os
            details['browser'] = browser

            data['context'].append({
                'ip': ip,
                'datetime': createdDateTime,
                'lat': lat,
                'lng': lng,
                'details': details
            })

        data['records_in_context'] = str(temp_count)

        data_master.append(data)

    print("\nWriting to data.json!")
    with open('data.json', 'w+') as outfile:
        json.dump(data_master, outfile, indent=4)

    print("Data collection complete!")


else:
    print(result.get("error"))
    print(result.get("error_description"))
