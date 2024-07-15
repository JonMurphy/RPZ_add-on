# commit

add RPZ as a new add-on

## What is it?
Response Policy Zone (RPZ) is a mechanism that makes it possible to define local policies in a standardised way and load policies from external sources.  RPZ has been part of the IPFire world since 2015 and is part of the current unbound setup.  

The RPZ add-on wakes up (enables) RPZ functionality with 2 lines in a configuration file.  The add-on simply adds a configuration file and adds three scripts (config, metrics and sleep) to make RPZ easier for the admin to use.

See:
https://en.wikipedia.org/wiki/Response_policy_zone
https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html


The base functionality of RPZ blocking DNS is similar to piHole but without the pretty graphics.  (there are no plans to add the pretty grphics).

## Why is it needed?
Some IPFire admin's utilize pi-hole to block unwanted websites via DNS lookup.  





I beleive enabling the URL filter has a similar effect of blocking unwanted websites.  


## What are the use cases?



