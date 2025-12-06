# Response Policy Zones (RPZ)

*** DRAFT *** work in progress *** DRAFT *** work in progress *** DRAFT *** work in progress *** DRAFT *** work in progress *** DRAFT *** 

Response Policy Zone (RPZ) is a mechanism that makes it possible to define local policies in a standardized way and load policies from external sources.  [^1]

The base functionality of RPZ blocking DNS is similar to piHole but without the pretty graphics.  (there are no plans to add the pretty graphics).

**Note**: Domains blocked by RPZ are not DROPped or REJECTed like when using a Firewall Rule. RPZ only blocks the domain name lookup. If a user decides to enter an IP address to get to their favorite site, RPZ will not stop it from happening. If this is needed I suggest using [IP Address Blocklists](https://www.ipfire.org/docs/configuration/firewall/ipblocklist).


## Installation

**Note**: The [test](https://community.ipfire.org/uploads/short-url/znjX2snktgFccQiem20CbYeky3z.tar) version of the RPZ add-on is installed manually until approved by the IPFire Developers.

Copy the `rpz-beta-0.1.nn-nn.ipfire.tar` file to the `/opt/pakfire/tmp/` directory.  **Please speak up if you need assistance with this!**

Then:
```bash
# 1 - set filename
fileName="rpz-beta-0.1.nn-nn.ipfire.tar"

# 2 - go to this directory:
cd /opt/pakfire/tmp/

# 3 - download file
wget https://github.com/JonMurphy/RPZ/raw/refs/heads/main/"${fileName}"

# 4 - uncompress the file:
tar xvf "${fileName}"

# 5 - check to make sure there are files there:
ls -l /opt/pakfire/tmp

# 6 - copy this one file to a new location
/bin/cp --verbose ROOTFILES /opt/pakfire/db/rootfiles/rpz

# 7a - install RPZ
NAME=rpz ./install.sh

# 7b - or upgeade RPZ
NAME=rpz ./install.sh
```


## Usage via WebGUI
The RPZ WebGUI is here thanks to Leo Hofmann!

To open the RPZ WebGUI go to menu **IPFire** > **Response Policy Zones (RPZ)**:

<p align="center">
  <img width="800" alt="rpz_webgui_menu" src="https://github.com/JonMurphy/RPZ/blob/7ae01fea833fc02d6e7d563f2e54eb881b973cff/docs/images/rpz_webgui_menu.png" />
</p>

## Zonefiles section
List of the Names, URLs, and a short Remark for each zonefile item.  There are 10 items maximum.  Too many lists will slow down Unbound and DNS.

### Add new line
To add a new RPZ list click on **Add** in the lower right corner of the Zonefiles section. 
![](./rpz_add_apply1.png "click Add")

Add a Name and the URL of a RPZ list.  A small remark can also be added.  Then click **Save**.
![](./rpz_edit_zonefiles_entry.png "example Edit window")

Multiple adds or edits can be done at one time (before clicking **Apply**)

**Note**: Remember to press **Apply** after you have finished your modifications.  The **Apply** sends an `unbound-control reload` which loads the various RPZ configuration files.
![](./rpz_apply.png "Do not forget to click Apply")

### Edit an existing line
Click on the pencil (Edit) on the needed line.
![](./rpz_zonefile_item.png)

Make the needed changes and  then click **Save**.
![](./rpz_edit_zonefiles_entry.png "example Edit window")

Multiple adds or edits can be done at one time (before clicking **Apply**)

**Note**: Remember to press **Apply** after you have finished your modifications. The **Apply** sends an `unbound-control reload` which loads the various RPZ configuration files.

![](./rpz_apply.png "Do not forget to click Apply")


## Custom lists section
List of allowlist domains and blocklist domain.  Loads the custom allow/block list into unbound RPZ. 

![](./rpz_custom_lists.png "example custom lists")
Domains are in this format:
```
*.com
*.domain.com
*.sub-domain.domain.com
*.sub.sub-domain.domain.com

domain.com
sub-domain.com
sub.sub-domain.domain.com
```

### Allowlist
At times an outside RPZ list will block a needed website. Allowed items can be added to this list.

### Blocklist
The block list operates in a similar way as the allowlist.

Make the needed changes to the custom allow/block lists and then click **Save**.
![](./rpz_custom_save2.png)

Multiple adds or edits can be done at one time (before clicking **Apply**)

**Note**: Remember to press **Apply** after you have finished your modifications.
![](./rpz_custom_apply2.png "do not forget to click Apply")


##  Logging
RPZ logging can be found in the unbound logs.  Go to **Logs** > **Systems Logs**, then click on **DNS: Unbound** in the drop-down, and then click the **Update** button.
![](./system_log_unbound_rpz.png "example of RPZ in system logs")

### Notes
 1. Large RPZ files will slow down the unbound reload time and slow down a DNS lookup.  Over 500,000 lines of RPZ files (total lines for all RPZ files) is discouraged. Over 1,000,000 lines of RPZ files (total lines for all RPZ files) is NOT recommended.
    - the Hagezi Threat Intelligence Feed (largest size) is **NOT** recommended due to it's large size (lines = 1,354,431)
        - Hagezi TIF medium or TIF mini should be fine.
    - the Hagezi Gambling (largest size) is **NOT** recommended due to it's large size (lines = 937,035)
        - Hagezi Gambling medium or Gambling mini should be fine.

 2. Keep in mind there may be overlap between an RPZ list and a list offered in [IP Address Blocklists](https://www.ipfire.org/docs/configuration/firewall/ipblocklist).  Please review the lists chosen before activating.

 3. Each RPZ file begins with a SOA record defining the update rate. Tests show that unbound defines a downcounter for the 'automagical' update of the file. A reload operation of unbound resets these counters. Therefore a reload period shorter than a specific update time disables the auto update of this RPZ file.
    * Defining or removing RPZ config files restarts unbound!


## Recommended RPZ lists
 1. [Hagezi - DNS Blocklists](https://github.com/hagezi/dns-blocklists?tab=readme-ov-file#zap-dns-blocklists---for-a-better-internet)
 2. [ThreatFox - DNS Response Policy Zone (RPZ)](https://threatfox.abuse.ch/export/#rpz)
 3. [URLHaus - DNS Response Policy Zone (RPZ)](https://urlhaus.abuse.ch/api/#rpz)
 4. [jpgpi250 - DNS block list for DoH](https://github.com/jpgpi250/piholemanual/blob/master/DOH/DOH.rpz)


## RPZ console commands
See the RPZ console commands here --> [Using the RPZ Console](./rpzconsole)


## Links
 * [dnsrpz.info - DNS Response Policy Zones](https://dnsrpz.info)
 * [Wikipedia - Response policy zone](https://en.wikipedia.org/wiki/Response_policy_zone)
 * [unbound - Response Policy Zones](https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html)


[^1]: [https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html](https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html)
