# commit

RPZ: install new add-on

### What is it?
Response Policy Zone (RPZ) is a mechanism to define local policies in a standardised way and load those policies from external sources.  Bottom line: RPZ allows admins to easily block access to websites via DNS lookup.

RPZ can block websites via categories.  Examples include: fake websites, annoying pop-up ads, newly registered domains, DoH bypass sites, bad "host" services, maliscious top level domains (e.g., *.zip, *.mov), piracy, gambling, pornography, and more.  RPZ lists come from various RPZ providers and their available 
catagories.

This RPZ add-on enables the RPZ functionality by adding a couple lines in a configuration file.  This add-on simply adds a configuration file and adds three scripts (config, metrics and sleep) to make RPZ easier for the admin to use.

RPZ was release in 2010 and has been part of the IPFire build since ~2015.

### Why is it needed?
Some IPFire admin's utilize pihole to block unwanted websites via DNS lookup.  Moving the base functionality (without pretty graphs) of pihole to IPFire removes one device from the admin's local network. (and hopefully this reduces the pihole questions from the Community for an unsupported device.)

The list RPZ providers can be recommended by IPFire and coded into a set list.  Or, if prefered, the local admin can choose their own RPZ providers.

### What are the use cases?
 * simple replacement for pihole base functionality
 * when admin sets the IPFire proxy to transparent mode, RPZ is a simple replacement for the URL Filter 

### IPFire Wiki
In process at: https://www.ipfire.org/docs/addons/rpz

### more info:
 * https://en.wikipedia.org/wiki/Response_policy_zone
 * https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html

### Need help with...
1) The custom allow and block lists are currently located at `/var/ipfire/rpz`.  Is this correct?
2) The three bash scripts are currently located at `/usr/sbin`.  Is this correct?

