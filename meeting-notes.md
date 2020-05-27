# § Meeting Notes [1]

> 8 May 2020

## Briefing:
During this meeting, we met with our Senior Security Analyst Jeffrey Rowe to discuss the overall goal of the project and any relevant technologies/APIs we will require.

From our proposal:
> Our tool will be used in the detection of compromised UC Davis accounts by analyzing connection logs and delivering a quantitative, ranked score to reflect our tool's confidence that a given account is truly compromised. The score will be based on a selected set of risk assessment features.

> In our initial prototype, we will primarily utilize spatio-temporal analysis of user session data to deliver an initial risk level, and will incorporate secondary risk assessment features in subsequent versions to improve the accuracy of the risk level calculation.

## Specifics:
One of the biggest problems we have regarding compromised account identification is filtering through false positives. Microsoft Azure Identify Protection flags accounts as "compromised" primarily on login location, which isn't very helpful for a university with such a large global presence. This issue is further complicated by remote instruction, as the frequency of foreign logins has greatly increased as a result. For these reasons, we have identified the primary data to analyze as *the time difference between subsequent logins and their respective geolocations*, which we will refer to as *Delta T and Geolocation*.

Our primary algorithm will be developed to perform this spacio-temporal analysis and assign a weighted value to each account. This will take into account the following:
 - previous account activity from foreign nations
 - realistic flight travel times
 - unusual travel activity
	 - To elaborate, the algorithm would differentiate a single, occasional flight to, say, London, versus nearly daily flights. It makes more sense to see an occasional login from abroad, but abnormally frequent back-and-forth travelling, even with legitimate travel times, would increase the risk level.
 - patterns in time of day
 - country risk level based on previously collected data
	 - For example, almost 70% of network traffic on the Library VPN comes from China, as many international students continue to use the VPN during university holidays and remote instruction.

To further improve the accuracy of the risk level, we have identified the following secondary risk assessment features to use for this project (subject to change):
 - carrier/device patterns
	 - This data will be extracted from the [MaxMind](https://www.maxmind.com/en/home) database.
 - respective CAS account activity
	 - the reason for this is to provide additional context to any potentially suspicious activity seen through Azure. For example, if an account has various logins detected by Azure and zero logins from CAS, this would mean that the account is only being accessed by Office 365. This would immediately be flagged as **suspicious**, because hackers often target University accounts to be able to distribute scam from officially registered @ucdavis accounts to members of specific departments, making it more likely for the target of the scam to fall for it.
 - password reset history

Our final algorithm will then assign unique weights to the severity of the suspicious activity (i.e. sporadic account activity from across multiple nations would be more severe than unusual carrier/device patterns). These will then be used to construct a *time-progressive n-dimensional map* of the various risk factors and their weights. **Details regarding this will be discussed in our next meeting.**

To get the final risk score, a simple distance calculation will be done on the map.

## Technology/API:

| Service              | Completed Setup?    |
| -------------------- |:-------------------:|
| Elastic Stack        | Yes                 |
| Microsoft Graphs API | No                  |
| MaxMind DB           | Yes                 |

**Elastic Stack (a.k.a. ELK Stack) API:** All network traffic crossing the North-South border at UC Davis is stored as Corelight "Bro" logs (now know as "Zeek" logs). These logs are then fed into Logstash (a data ingestion tool), which filters and transforms the logs, before storing them in their respective clusters. Elasticsearch, a RESTful search engine, analyzes them according to specified rules. At this point in the stack, the logs are ready to be visualized by Kibana, a data visualization tool. Within Kibana, the various types of network logs can be analyzed by human security analysts, most commonly as evidence for various security incidents.

For this project, we will be extracting a significant chunk of our data from the ELK Stack, as well as introducing a new type of data to the stack: our calculated risk score.

**MaxMind DB:** MaxMind is an provider of IP intelligence and fraud prevention tools. We will be using MaxMind's GeoIP databases to determine geolocation and carrier information tied to each investigation. We will implement this data through the ELK Stack so that nearly all of the data to be analyzed would be accessible through the same API calls.

**Microsoft Graphs API:** To retrieve Office 365 account activity, we will be using Graphs API to interface with Microsoft Azure. We plan on integrating this into the ELK Stack as well.

## Current Progress:

This is found in our milestones.md file.
