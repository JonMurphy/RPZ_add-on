# commit

RPZ congig: New add-on

## What is it?
Response Policy Zone (RPZ) is a mechanism that makes it possible to define local policies in a standardised way and load those policies from external sources.  RPZ allows admins to easily block access to a website via DNS lookup.

RPZ can block websites via categories and examples include: fake websites, annoying pop-up adds, newly registered domains, DoH bypass sites, bad "host" services, maliscious top level domains (i.e., *.zip, *.mov), piracy, gambling, pornography, and more.  This is dependent on the RPZ provider and the catagories chosen.

This RPZ add-on wakes up (enables) the RPZ functionality by adding 2 lines in a configuration file.  The add-on simply adds a configuration file and adds three scripts (config, metrics and sleep) to make RPZ easier for the admin to use.

RPZ has been avaialble since 2010 and has been part of the IPFire build since ~2015.

more info:
https://en.wikipedia.org/wiki/Response_policy_zone
https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html


## Why is it needed?
Some IPFire admin's utilize pi-hole to block unwanted websites via DNS lookup.  

The base functionality of RPZ blocking DNS is similar to piHole but without the pretty graphics.  (there are no plans to add the pretty grphics).




I beleive enabling the URL filter has a similar effect of blocking unwanted websites.  


## What are the use cases?



