---
layout: markdown
title: Client Fingerprinting
permalink: /client-fingerprinting/

header: Client Analysis
subheader: 
---


There's no inherent way to know exactly what client a validator is running. Researchers use other metrics to make deductions on which client a validator is most likely operating. The problem is they cannot distinguish with 100% certainty which client a validator is running.

<strong>Miga Labs</strong> uses a crawler to count beacon nodes and their self-reported identity. However, this means that validators sharing a node are counted only once and nodes with fewer validators have a greater influence on the estimate. ([Miga Labs {{site.data.icons.new_tab}}](https://migalabs.es/))

Another method developed by <strong>Sigma Prime's Michael Sproul</strong> is to analyze each client's block proposal style as described in [this tweet thread](https://twitter.com/sproulM_/status/1440512518242197516).

