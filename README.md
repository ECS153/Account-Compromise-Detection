# Final Project - The SoC
> Andrikanis, Nikita

> Muldoon, Kyle
> 
## Account Compromise Detection Tool

Our project was done in 2 Phases:
 - Data collection and processing
 - Algorithm

The scripts in *./data_collection* were used to collect data from Microsoft Azure and MaxMind DB, building a *data.json* of potentially risky users and their corresponding contextual data. In *./ranking*, we have our algorithm scripts. These take in *data.json* and perform our analysis. The final ranked list is then returned to the console.

#### [*data_collection_AZURE.py*](https://github.com/ECS153/final-project-the-soc/blob/master/Account%20Compromise%20Detection/data_collection/data_collection_AZURE.py)
This script builds our queries to Microsoft Azure using Graphs API. First, the top 20 users are collected from Azure's unranked list based on most recently updated risk. For each user, we send an additional query to obtain all of the user's activity from the last 14 days. To obtain GeoIP, we query MaxMind DB. This data is then compiled into *data.json*, which is now ready for analysis.
 
 #### [*mmdb_lookup.py*](https://github.com/ECS153/final-project-the-soc/blob/master/Account%20Compromise%20Detection/mmdb_lookup.py)
This script is called by *data_collection_AZURE.py*. Originally, it sent queries to the MaxMind Web Database to obtain accurate GeoIP data for each IP we provided. In this final version, we were able to download local databases from MaxMind, speeding up the data collection process significantly. These databases are located in *./databases*.

#### [*geo-ip-verifier.py & geoip-tester.py*](https://github.com/ECS153/final-project-the-soc/tree/master/Account%20Compromise%20Detection/data_collection)
These two scripts were used during the first week of development. Over the past few months of manual account compromise investigations, we noticed that Azure's GeoIP data is often inaccurate. We used these scripts to test the true accuracy of Azure's location data as compared to our trusted source: MaxMind. We were able to confirm the inaccuracy. For this reason, we acquired the local databases from MaxMind to allow us to use their GeoIP data exclusively.

#### [*algorithm.py*](https://github.com/ECS153/final-project-the-soc/blob/master/Account%20Compromise%20Detection/ranking/algorithm.py)
This script takes *data.json* as an argument. It first calls a utility function to build the master table, in which the contextual data for each user is stored. It then performs the weighted sum calculation by calling a series of utility functions. After the calculation, the output is built in a JSON-like format, sorted in descending order, and outputted to the console for the security analyst to use.

#### [*utilities.py*](https://github.com/ECS153/final-project-the-soc/blob/master/Account%20Compromise%20Detection/ranking/utilities.py)
All of our utility functions are found here. In addition to the master table builder (which formats the data for *algorithm py* to analyze), there are four functions for each of our security features: spatio-temporal, VPN behavior, user agent, and client app analyses. The outputs are *unweighted*. These scores are then returned to *algorithm py*, which applies the unique weights and completes the final score calculation.

## Experimental Results
In addition to the source code, we provided the contextual data that the algorithm uses to perform its analysis in *data.json*. This data was captured on 8 June 2020.

First, we took the 20 most recently flagged users from Azure. Before running the algorithm, we performed our manual investigations. Please see [*humanQualitativeAnalysis.txt*](https://github.com/ECS153/final-project-the-soc/blob/master/Account%20Compromise%20Detection/humanQualitativeAnalysis.txt). In it, we described our manual investigation process; notice our brief notes and final verdicts of each investigation. The string of characters preceding each analysis is a random string generated to obfuscate the true identity of the user. When performing our analysis, almost all of the 20 user were compromised (we usually get many more false positives; since we're using real data, we had to deal with what we were given). This, however, made it more interesting when analyzing this list of risky users, because each user has a varying **degree of compromise**; some are more severe than others. For example, some accounts actively use the Library VPN. If this user is compromised, it could have more severe implications for the university than an account that, for example, belongs to a graduated student and is no longer in use.

We then compared these results against the algorithm output, found in [*sampleRun txt*](https://github.com/ECS153/final-project-the-soc/blob/master/Account%20Compromise%20Detection/sampleRun.txt). The script confirmed nearly all of our verdicts, including those with higher severity and the false positive at the bottom of the list. The questionable users were appropriately ranked towards the lower half of the ranked list.

Moving forward into the summer, we plan on continuing to tune our algorithm to increase its accuracy. We will also apply Machine Learning, tapping into the historic data stored on our servers for models. Our ultimate goal with this project is to deliver a fully stand-alone app that performs risk analysis regardless of platform (i.e. Azure, Google, etc.).

And this concludes our project!
