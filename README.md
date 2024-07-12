# RPZ - Response Policy Zones
Response Policy Zone (RPZ) is a mechanism that makes it possible to define local policies in a standardised way and load  policies from external sources.  [^1].  The base functionality of blocking DNS is similar to piHole but without the pretty graphics.  (there are no plans to add the pretty grphics).

Note: Domains blocked by RPZ are not DROPped or REJECTed like when using a Firewall Rule. RPZ only blocks the domain name lookup. If a user decides to enter an IP address to get to their favorite site, RPZ will not stop it from happening. If this is needed I suggest using [IP Address Blocklists](https://www.ipfire.org/docs/configuration/firewall/ipblocklist).


## Installation
Note: The test version of the RPZ add-on is installed manually until approved by the IPFire Developers.  It is installed similar to this method:

https://www.ipfire.org/docs/devel/ipfire-2-x/addon-howto#testing-the-install-uninstall-update-routines-and-add-on-itself

<strike>
	
rpz can be installed with the Pakfire web interface or via the console:

```bash
pakfire install rpz
```
</strike>


## Usage
There is no web interface for this add-on. To run this add-on open the serial console, or the local terminal and access the IPFire box via SSH.  There are three simple scripts available for set-up:

[rpz-config](RPZ%20wiki.md) - Create, remove or make an external RPZ file 

[rpz-metrics](RPZ%20wiki.md) - Locates RPZ names from the message logs and sort by hits.  Selecting all logs (1 year) may take ~60 seconds to complete.

[rpz-sleep](RPZ%20wiki.md) - Disable the RPZ for a NUMBER of seconds (default 5 minutes).

PS - I am looking for someone to assist with a WebGUI.

### Create a config file for RPZ
The `rpz-config` script assists in creating, deleting or builing RPZ files.

```
Usage: 	rpz-config  <action> <name> <url>

Actions:
add <name> <url>        adds new RPZ config file by RPZ name
remove <name> <url>     removes unneeded RPZ files by RPZ name
  <name>                unique alpha-numeric name for the RPZ file.  This name appears in the message log and
                          is the basename for the config file. e.g., threatfox, urlhaus, PopUpAdsHZ
  <url>                 URL for RPZ.  Must be in a format similar to https://example.com/path/filename.
                          Other protocols such as file://, ftp://, etc. will not work.
make <allow or block>   build the custom allow or block RPZ files
```

Example commands:
```
rpz-config add MxUltimateHZ https://raw.githubusercontent.com/hagezi/dns-blocklists/main/rpz/ultimate.txt

rpz-config remove MxUltimateHZ

rpz-config make allow
```
Example response:
<img width="1005" alt="Screen Shot 2024-07-04 at 4 51 13 PM" src="https://github.com/JonMurphy/RPZ/assets/15616372/a27f74b6-db45-4e91-a307-3ddb55cb82e2">

#### Custom allow list or block list
The `rpz-config make allow` script loads the custom allow list into unbound RPZ.

#### Allow list
Sometimes outside RPZ lists will block a needed website.  Allowed items can be added to this list.

Edit the `/var/ipfire/rpz/allowlist` and add the needed websites:
<img width="981" alt="Screen Shot 2024-07-04 at 4 08 32 PM" src="https://github.com/JonMurphy/RPZ/assets/15616372/6c21e799-a3d5-4a6f-8c66-4875e51d0b7e">

#### Block list
The block list operates in a similar way as the allow list and is located at `/var/ipfire/rpz/blocklist`:
<img width="977" alt="Screen Shot 2024-07-04 at 4 23 13 PM" src="https://github.com/JonMurphy/RPZ/assets/15616372/0a35b5e7-fb0e-413b-aaa7-cd9a5da3f969">

**Note**: whenever a RPZ file is added, removed, or built the upbound reload (i.e., `unbound-control reload`) is run.  This loads all of the new settings.  Keep in mind this may pause DNS up to ~60 seconds depending on the size of the RPZ files.  Large RPZ files will slow down the unbound reload time and slow down a DNS lookup.  Over 1,000,000 lines of RPZ files (total lines for all RPZ files) is NOT recommended.

### Metrics of RPZ usage
The `rpz-metrics` script searches the message logs for RPZ names and sorts those names by the number of hits.  Selecting all message logs (1 year or 53 message log files) may take ~60 seconds to complete.

```
Usage: 	rpz-metrics <number of message logs>
    default <number of message logs> is 2
```

Example response:
<img width="977" alt="Screen Shot 2024-07-04 at 9 49 32 PM" src="https://github.com/JonMurphy/RPZ/assets/15616372/63b2adf5-cbaf-4c4f-9011-301e60898e82">

### Pause RPZ for N time
Pause for NUMBER seconds. SUFFIX may be 's' for seconds, 'm' for minutes, 'h' for hours or 'd' for days.
```
Usage: 	rpz-sleep <sleep time>
    default <sleep time> is 5 minutes
```

Example response:
<img width="977" alt="342118230-9f753be5-80d7-4da5-8e56-023829207185" src="https://github.com/JonMurphy/RPZ/assets/15616372/d86d41d2-ded9-4025-b359-1af113438a61">


## Recommended RPZ lists
 1. https://github.com/hagezi/dns-blocklists
 2. https://threatfox.abuse.ch/export/#rpz
 3. https://urlhaus.abuse.ch/api/#rpz


## Links
 * https://en.wikipedia.org/wiki/Response_policy_zone
 * https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html
 * https://github.com/jpgpi250/piholemanual/blob/master/doc/Unbound%20response%20policy%20zones.pdf

[^1]: https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html

#### Known issues
 * The current unbound bridge causes frequent unbound restarts and may cause the RPZ list updates to be delayed by a day or three.
 * Large RPZ files will slow down the unbound reload time and slow down a DNS lookup.  Over 500,000 lines of RPZ files (total lines for all RPZ files) is discouraged. Over 1,000,000 lines of RPZ files (total lines for all RPZ files) is NOT recommended.
