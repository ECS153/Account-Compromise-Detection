###################################################################################
# Utility functions
#   - These functions calculate the scores for each of our 4 key security features
###################################################################################

import math
import mpu
import re
import datetime
import ipaddress

class Location:
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng


# Return the distance between two locations on earth, defined by lat / lon. Accepts 2 Location objects
def distance_lat_long(l1: Location, l2: Location):
    distance = mpu.haversine_distance((l1.lat, l1.lng), (l2.lat, l2.lng))
    return distance


#######################
# algorithm functions
#######################

def build_evidence_table(data):
    master_table = []

    for user in data:
        user_row = {}
        user_row['userId'] = user['id']
        user_row['logCount'] = user['records_in_context']
        user_row['signInLogs'] = []
        for signInEvent in user['context']:
            connection_event = {}
            connection_event['ip'] = signInEvent['ip']
            connection_event['datetime'] = signInEvent['datetime']
            connection_event['latlng'] = Location(signInEvent['lat'], signInEvent['lng'])
            connection_event['clientApp'] = signInEvent['details']['clientAppUsed']
            connection_event['userAgent'] = signInEvent['details']['userAgent']
            connection_event['os'] = signInEvent['details']['os']
            connection_event['browser'] = signInEvent['details']['browser']
            # Append to user's individual table
            user_row['signInLogs'].append(connection_event)
        # Append to master table holding all users
        master_table.append(user_row)

    return master_table


def time_space_analysis(user):
    user_si_logs = user['signInLogs']


    ############################################################################
    #  Generate DeltaPairs tuples for all sign in events, containing [delta(distance, time), ...]
    ############################################################################
    deltaPairs = []
    for i in range(len(user_si_logs) - 1):
        loc1 = user_si_logs[i]['latlng']
        loc2 = user_si_logs[i + 1]['latlng']

        # Input format: "2020-05-08T11:52:16.1521821Z"
        t1 = user_si_logs[i]['datetime']
        t2 = user_si_logs[i + 1]['datetime']

        t1_split = re.split('[TZ]|-|:|\.', t1)
        t1_dt = datetime.datetime(int(t1_split[0]), int(t1_split[1]), int(t1_split[2]), int(t1_split[3]),
                                  int(t1_split[4]), int(t1_split[5]))

        t2_split = re.split('[TZ]|-|:|\.', t2)
        t2_dt = datetime.datetime(int(t2_split[0]), int(t2_split[1]), int(t2_split[2]), int(t2_split[3]),
                                  int(t2_split[4]), int(t2_split[5]))

        deltaD = distance_lat_long(loc1, loc2)
        deltaT = t1_dt - t2_dt

        deltaPairs.append([deltaD, deltaT])

    ############################################################################
    # Run analysis on each pair
    #   - calculate travel speed given delta values
    #   - compare against average flight speed
    #   - if greater than limit, flag
    #   - Ref: https://www.flightdeckfriend.com/how-fast-do-commercial-aeroplanes-fly
    #   - 740 – 930 kph
    #   - v = deltaD / deltaT
    ############################################################################

    for DT_pair in deltaPairs:
        D = DT_pair[0]
        T = (DT_pair[1].total_seconds()) / 3600.0

        # Colve for velocity, and account for logins at a finer grain resolution than 1 second
        if not T == 0:
            V = D/T
        else:
            V = D/(1.0/3600.0)

        # Check if user travelled faster than an airplane
        if V > 1000:
            DT_pair.append("suspect")
            percent_over_limit = (V - 1000) / V
            DT_pair.append(percent_over_limit)
        else:
            DT_pair.append("ok")
            percent_over_limit = (1000 - V) / (V + 0.00000001)
            DT_pair.append(percent_over_limit)

    ############################################################################
    # calculate proportion of logins that looked suspect overall
    ############################################################################

    susCount = 0
    totCount = 0
    for DT_pair in deltaPairs:
        if DT_pair[2] == "suspect":
            susCount += 1
            totCount += 1
        else:
            totCount += 1
            continue

    susPercent = susCount/totCount

    return susPercent


def check_vpn_usage(user, spacetime):
    user_si_logs = user['signInLogs']

    vpn_count = 0
    reg_count = 0
    for i in range(len(user_si_logs) - 1):
        ip = ipaddress.ip_address(user_si_logs[i]['ip'])
        if ip in ipaddress.ip_network('128.120.234.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('128.120.235.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('128.120.236.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('128.120.237.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('128.120.238.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('128.120.239.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('128.120.251.0/24'):
            vpn_count += 1
        elif ip in ipaddress.ip_network('169.237.45.0/24'):
            vpn_count += 1
        reg_count += 1

    # proportion of logins that used the ucd vpn network
    proportion = vpn_count/reg_count

    if proportion > 0:
        if spacetime > 0.15:
            proportion = proportion + 0.15
        else:
            proportion = proportion - 0.15

    return proportion


def user_agent_analysis(user):
    # generate a list containing unique user agents for a particular user
    user_agents = []
    for si_log in user['signInLogs']:
        if si_log['userAgent'] not in user_agents:
            user_agents.append(si_log['userAgent'])

    user['uniqueAgents'] = user_agents

    numAgents = user_agents.__len__()
    score = 0

    if numAgents in range(5, 10):
        score = 1
    elif numAgents > 9:
        score = 2


    return score


def client_app_analysis(user):
    # generate a list containing unique client apps for a particular user
    user_client_apps = []
    for si_log in user['signInLogs']:
        if si_log['clientApp'] not in user_client_apps:
            user_client_apps.append(si_log['clientApp'])

    user['uniqueClientApps'] = user_client_apps

    numApps = user_client_apps.__len__()
    score = 0


    if 'IMAP4' in user_client_apps:
        score = 0.5

        if numApps in range(1, 3):
            score = 2

    return score

