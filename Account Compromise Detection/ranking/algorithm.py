##############################################################
# The algorithm script, essentially our tool's "main"
#   - This script calculates the weighted sum for each user
##############################################################

import json
from ranking.utilities import *

####################
# Environment set-up
####################
# Open data.json location
data_path = "../data_collection/data.json"
data = json.load(open(data_path))


#######################
# Build evidence table
#######################
master_table = build_evidence_table(data)

################################################################
# Run algorithm loop for each user, buld a report for each one
################################################################

# INVESTIGATE EACH USER, ADD NEW CALCULATIONS BACK TO USER INVESTIGATION
for user in master_table:
    user_report = {}

    # calculate proportion of suspect Time-Space cases out of all logins
    user_report['timeSpaceScore'] = time_space_analysis(user) * 5

    # calculate what proportion of logins used by a UCD VPN
    user_report['VPNScore'] = check_vpn_usage(user, user_report['timeSpaceScore'] / 5)

    # find number of unique user agents
    user_report['userAgentScore'] = user_agent_analysis(user) * 1

    # find number of unique client apps during the time
    user_report['clientAppScore'] = client_app_analysis(user) * 1

    weighted_sum = 0

    for score in user_report:
        weighted_sum += user_report[score]

    user_report['WeightedSum'] = weighted_sum

    user_report['userId'] = user['userId']

    user['userReport'] = user_report



###################################################
#  Provide sorted list (descending) of risky users
###################################################

unsorted_reports = []

for user in master_table:
    unsorted_reports.append(user['userReport'])

sorted_reports = sorted(unsorted_reports, key = lambda i: i['WeightedSum'], reverse = True)

for user_report in sorted_reports:
    print("USER: " + user_report['userId'] + "\tScore: " + str(user_report['WeightedSum']))
    print("{\n\tTIMESPACE: " + str(user_report['timeSpaceScore']) + "\n\tVPN: " + str(user_report['VPNScore']) +
          "\n\tUSERAGENT: " + str(user_report['userAgentScore'])  + "\n\tCLIENTAPPS: " +
          str(user_report['clientAppScore']) + "\n}\n")

