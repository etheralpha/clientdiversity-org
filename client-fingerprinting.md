---
layout: markdown
title: Client Fingerprinting
permalink: /client-fingerprinting/

header: Client Analysis
subheader: 
---

There's no inheret way to know exactly what client a validator is running. Researchers use other metrics to make deductions on which client a validator is most likely running.

Miga Labs analyzes the machine resource consumption based on the PID of the processes without revealing any information about the blockchain, node or host. [[Read more](https://migalabs.es/eth2-client-analyzer/)]

Another method developed by Lighthouse's Michael Sproul is to analyze each client's block proposal style as described in [this tweet thread](https://twitter.com/sproulM_/status/1440512518242197516).

<!-- It's important for clients not to broadcast which client they are in order to minimize potential for client-based attacks. -->