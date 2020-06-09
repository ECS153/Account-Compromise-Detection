# Final Project - The SoC
> Andrikanis, Nikita
> Muldoon, Kyle
> 
## Account Compromise Detection Tool

Our project was done in 2 Phases:
 - Data collection and processing
 - Algorithm

The scripts in *./data_collection* were used to collect data from Microsoft Azure and MaxMind DB, building a *data.json* of risky user IDs and their corresponding contextual data. In *./ranking*, we have our algorithm scripts, that take in the *data.json* file and perform our analysis. The final ranked list is then returned to console.

#### *data_collection_AZURE py*
 This script builds our queries to Microsoft Azure using Graphs API. First, the top 20 users are collected from Azure's unranked list based on most recently updated risk. For each user, we send an additional query to obtain all of the user's activity from the last 14 days. To obtain GeoIP, we query MaxMind DB. This data is then compiled into *data.json*, which is now ready for analysis.
 
 #### *mmdb_lookup py*
This script is called by *data_collection_AZURE.py*. Originally, it sent queries to the MaxMind Web Database to obtain accurate GeoIP data for each ip we provided. In this final version, we were able to obtain local databases from MaxMind, speeding up the data collection process significantly. These databases are located in *./databases*.

#### *geo-ip-verifier py & geoip-tester py*
These two files were used during the first week of development. Over the past few months of account compromise investigations, we noticed that Azure's GeoIP data is often inaccurate. We used these scripts to test the true accuracy of Azure's location data as compared to our trusted source: MaxMind. We were able to confirm the inaccuracy. For this reason, we acquired the local databases from MaxMind to allow us to use their GeoIP data exclusively.

#### *algorithm py*
This script takes *data.json* as an argument. It first calls a utility function to build the master table, in which the contextual data for each user is stored. It then performs the weighted sum calculation by calling a series of utility functions. After the calculation, the output is build in a JSON-like format, sorting in descending order, and outputted to the console.

#### *utilities py*
All of our utility functions are found here. In addition to the master table builder, there are four functions for each of our security features: spatio-temporal, VPN, user agent, and client app analyses. The outputs are *unweighted*. These scores are then returned to *algorithm py*, which applies the unique weights and completes the final score calculation.

## Experimental Results
In addition to the source code, we provided the contextual data that the algorithm uses to perform its analysis in *data.json*.

First, we took the top 20 most recently flagged risky users. Before running the algorithm, we performed our manual investigations. In *humanQualitativeAnalysis txt*, notice our brief notes and final verdicts of each investigation. The string of characters preceding each analysis is a random string generated to obfuscate the true identity of the user. When performing our analysis, almost all of the 20 recent risky users were compromised (we usually get many more false positives; since we're using real data, we had to deal with what we were given). This, however, made it more interesting when analyzing this list of risky users, because each user has a **degree of compromise**; some are more severe than others.

We then compared these results against the algorithm output, found in *sampleRun txt*. The script confirmed nearly all of our verdicts, including those with higher severity and the false positive at the bottom of the list.

Moving forward into the summer, we plan on continuing to tune our algorithm to increase its accuracy. We will then apply Machine Learning and seeing where it would take us from there. Our ultimate goal with this project is to deliver a fully stand-alone app that performs risk analysis regardless of platform (i.e. Azure, Google, etc.).

And this concludes our project!
