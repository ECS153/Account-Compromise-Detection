
# § Milestones

------

> Milestone 3
> 26 May 2020

**[Recap Video 3](https://www.youtube.com/watch?v=u0Wd7o9tq_M)

Progress:
- Completed our data pipeline to capture data from both MS Azure and our ELK log systems to populate tables for each risky user. These are fully loaded into the algorithm script with as small overhead as we could get.
- After running some statistical analysis on the Azure geoip, we found that its geoip database is much less frequently updated than Maxmind Geoip2 Database. For this reason, our data collection pipeline now includes the use of Maxmind Database as our source of location data for any given IP address.
- As per your suggestion, we implemented User Agent data as an additional threat intel source. This is provided by Maxmind as well.
- Finally, we fully implemented our first-iteration of the spacio-temporal analysis script. After continuing to implement additional risk factors into the algorithm, we will meet on Friday of this week to adjust the weights of each factor, tuning the final output.

WIP - Goals for the Week:
- Complete the score rating functions for each of our chosen factors.
- Using these individual components to calculate our aggregated, weighted sum.
- We were officially approved for our BastionHost account this morning (Tuesday morning), so we will be able to set up queries of ELK for CAS logs.
- Hold our end-of-week meeting on Friday to address weights of each risk factor and discuss the goals for the following week.

Blocks:
- Storing our newly generated logs within our ELK stack is going to be very intensive, and will not change what we deliver with our project; it will only help us do our job as analysts (all analysis will still be available). In other words, we will continue to use 2 separate query scripts for Azure and ELK, rather than pipelining Azure logs **into** ELK, and then using a single query to extract all data.

------

> Milestone 2
> 19 May 2020

**[Recap Video 2](https://www.youtube.com/watch?v=9X872PMz32w&feature=youtu.be)

Progress:
- Completed script to query Microsoft Azure for recent riskyUsers as are flagged by the preliminary risk assessment.
- Built a JSON data straucture of individual sign-ins related to each of the identified risky accounts.
- Implemented MaxMind DB query into the data collection script for additional contextual information for each investigation.
- Established initial time frame window for analysis: 14 days. This number will be adjusted during our end-of-the-week meetings based on test results.
- Completed simple optimizations to the data collection script to support very large data volumes. Will be done more thoroughly in the future.

Upcoming:
- 2 Main Phases we can work on simultaneously this week
    - We will begin writing out the risk-analysis algorithm. This will use Microsoft and MaxMind data.
    - Redirecting Microsoft and Azure data through the ELK stack pipeline to allow us to also use CAS logs for our algorithm. This will make all of our data input/output through ELK.
- Define intergaces so that we can be data source agnostic as we add additional risk factors in the future and beyond.

Blocks:
- Our progress on redirecting data input through the ELK stack depends on when our BastionHost access is approved (expecting in the next 48 hours). Luckily, this doesn't affect our development of the algorithm itself.

------

> Milestone 1
> 12 May 2020


**[Recap Video](https://www.youtube.com/watch?v=PDeN6tICP9U&feature=youtu.be)**




**Summary:**
We had a meeting on 8 May 2020 to discuss the project goals, details, and technologies/API we would require. We identified an initial prototype, and what we plan on implementing for subsequent versions (as we plan on continuing to develop this project over the summer). The extensive meeting notes and design details are found here:

[meeting-notes.md on Github](https://github.com/ECS153/final-project-the-soc/blob/master/meeting-notes.md)

*To clarify our expected workflow and progress tracking*:
The majority of our work will be done at the IET Security Operations Center off-campus, as we must be on the office network to test our scripts with real data. Because of this, most of our progress will be as a group since we meet in person, rather than having multiple individual reports.

**Group Progress:**
(1) what you did last week:
 - Identified the specific technologies/API we will require for collecting data relevant to our project (outlined in meeting-notes linked above)
 - Identified expected project goals and overall project design
 - Set up Elastic Stack and MaxMind DB APIs to be ready to implement

(2) what you plan to do this week:
 - Finish building Microsoft Graphs API tool
 - Upload the code to our project Github

(3) anything that you’re stuck on:
 - nothing currently
