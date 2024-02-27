---
layout: markdown
title: Data Methodology
permalink: /methodology/
# redirect from the old path
redirect_from: /client-fingerprinting/

header: Data Methodology
subheader: 
---


There's no inherent way to know exactly what client a validator is running. Researchers use other metrics to make deductions on which client a validator is most likely operating. The problem is they cannot distinguish with 100% certainty which client a validator is running.


## Consensus Client Data

[Blockprint](https://blockprint.sigp.io/) - Developed by Sigma Prime's Michael Sproul, Blockprint  analyzes each client's block proposal style as described in [this Twitter thread](https://twitter.com/sproulM_/status/1440512518242197516) ([Nitter](https://nitter.snopyta.org/sproulM_/status/1440512518242197516)).

[Miga Labs](https://migalabs.io/) - A crawler is used to count beacon nodes and their self-reported identity. However, this means that validators sharing a node are counted only once and nodes with fewer validators have a greater influence on the estimate.

[Rated](https://www.rated.network/) - Methodology unknown.


## Execution Client Data

[Ethernodes](https://ethernodes.org/) - Methodology unknown.

{% assign supermajority = site.data.supermajority | last %}
{% assign supermajority_geth = supermajority.data.other.validators_percentage | times: 100 | round: 1 %}
{% assign supermajority_other = 100 | minus: supermajority_geth %}

[supermajority.info](https://supermajority.info) - Through social effort, supermajority.info (lead by Sonic) gathers **self-reported** client breakdown data and weighted against how many validators each entity has. This accounts for {{supermajority_geth}}% of the network. To estimate the remaining {{supermajority_other}}%, two steps were taken. The values that are "unknown" from the self-reported data are assumed to be 100% Geth. The remaining validators on the network are assumed to be 80% Geth and 20% split evenly among the other clients.
