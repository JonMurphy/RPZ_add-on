# commit

RPZ congig: New add-on

### What is it?
Response Policy Zone (RPZ) is a mechanism to define local policies in a standardised way and load those policies from external sources.  Bottom line: RPZ allows admins to easily block access to a website via DNS lookup.

RPZ can block websites via categories and some examples include: fake websites, annoying pop-up ads, newly registered domains, DoH bypass sites, bad "host" services, maliscious top level domains (i.e., *.zip, *.mov), piracy, gambling, pornography, and more.  This is dependent on the RPZ provider and the catagories chosen.

This RPZ add-on enables the RPZ functionality by adding 2 lines in a configuration file.  The add-on simply adds a configuration file and adds three scripts (config, metrics and sleep) to make RPZ easier for the admin to use.

RPZ has been avaialble since 2010 and has been part of the IPFire build since ~2015.

### Why is it needed?
Some IPFire admin's utilize pihole to block unwanted websites via DNS lookup.  Moving the base functionality (without pretty graphs) of pihole to IPFire removes one device from the admin's local network. (and hopefully this reduces the pihole questions from the Community for an unsupported device.)



And some admins utilize URL filter to block websites.

The base functionality of RPZ blocking DNS is similar to piHole but without the pretty graphics.  (there are no plans to add the pretty grphics).

https://www.ipfire.org/docs/addons/rpz

### What are the use cases?
 * simple replacement for pihole base functions
 * simple replacement for URL Filter if admin runs IPFire proxy in transparent mode

### IPFire Wiki
In process at: https://wiki.ipfire.org/addons/rsnapshot

more info:
https://en.wikipedia.org/wiki/Response_policy_zone
https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html
