# § The SoC - Proposal:

> Members: Nikita Andrikanis and Kyle Muldoon

### _Summary_:

Our tool will be used in the detection of compromised UC Davis accounts by analyzing connection logs and delivering a quantitative, ranked score to reflect our tool's confidence that a given account is truly compromised. The score will be based on a selected set of risk assessment features.

In our initial prototype, we will primarily utilize spatio-temporal analysis of user session data to deliver an initial risk level, and will incorporate secondary risk assessment features in subsequent versions to improve the accuracy of the risk level calculation.

### _Importance_:

Working in the Cybersecurity department for a major public university, account compromise is something we deal with daily. The number of incidents has recently exploded in the wake of the Chegg breach in late September 2019. The task of determining compromised accounts is very tedious and labor intensive for human analysts such as ourselves. Currently, we use Elastic Stack and Microsoft Azure to present us with a list of flagged accounts. However, this list is massive and unranked; every case is treated with an equal threat level, which often causes legitimately compromised accounts to be overlooked due to the volume of alert logs.

### _Expected Results_:

 Our goal with this tool is to create a ranked priority list of compromised accounts based upon a cumulative risk level. This number will be influenced by weighted risk factors from a set of selected risk assessment features.
With this, we would be able to more accurately classify truly malicious account behavior and significantly decrease the false positives count.
