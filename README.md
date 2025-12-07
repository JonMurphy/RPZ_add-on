# Response Policy Zones (RPZ)

**DRAFT : work in progress**

The Response Policy Zone (RPZ) is a mechanism that enables the definition of local policies in a standardized manner and facilitates the loading of policies from external sources. [^1]

The base functionality of RPZ blocking DNS is similar to piHole but without the pretty graphics (there are no plans to add the pretty graphics).

Domains blocked by RPZ are not **DROP**ped or **REJECT**ed like when using a Firewall Rule. RPZ only blocks the domain name lookup. If a user decides to enter an IP address to get to their favorite site, RPZ will not stop it from happening. If this is needed I suggest using [IP Address Blocklists](https://www.ipfire.org/docs/configuration/firewall/ipblocklist).


## Installation

The RPZ add-on (test version) is installed manually.  To install follow these steps:
```bash
# 1 - set filename
#fileName="rpz-beta-0.1.nn-nn.ipfire.tar"
fileName="rpz-beta-0.1.18-18.ipfire.tar"

# 2 - go to this directory:
cd /opt/pakfire/tmp/

# 3 - download file (still experimenting)
curl --silent --show-error --location https://github.com/JonMurphy/RPZ/raw/refs/heads/main/"${fileName}" -o rpz.ipfire

# 4 - uncompress the file:
tar xvf "${fileName}"

# 5 - check to make sure there are files there:
ls -l

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
  <img width="700" alt="rpz_webgui_menu" src="docs/images/rpz_webgui_menu.png" />
</p>


## Zonefiles section
List of the Names, URLs, and a short Remark for each zonefile item.  There are 10 items maximum.  Too many lists will slow down Unbound and DNS.

### Add new line
To add a new RPZ list click on **Add** in the lower right corner of the Zonefiles section. 

<p align="center">
  <img width="800" src="docs/images/rpz_add.png" alt="rpz_add" />
  <br />
  <small><em>click Add</em></small>
  <br />
</p>

Add a Name and the URL of a RPZ list.  A small remark can also be added.  Then click **Save**.

<p align="center">
  <img width="800" src="docs/images/rpz_edit_zonefiles_entry.png" alt="rpz_edit_zonefiles_entry" />
  <br />
  <small><em>example Edit window</em></small>
</p>

Multiple adds or edits can be done at one time before clicking **Apply**.

**Note**: Remember to press **Apply** after you have finished your modifications.  The **Apply** sends an `unbound-control reload` which loads the various RPZ configuration files.

<p align="center">
  <img width="800" src="docs/images/rpz_apply.png" alt="rpz_apply" />
  <br />
  <small><em>Do not forget to click Apply</em></small>
</p>

### Edit an existing line
Click on the pencil (Edit) on the needed line.

<p align="center">
  <img width="800" src="docs/images/rpz_zonefile_item.png" alt="rpz_zonefile_item" />
  <br />
  <small><em>click on pencil</em></small>
</p>

Make the needed changes and then click **Save**.

<p align="center">
  <img width="800" src="docs/images/rpz_edit_zonefiles_entry.png" alt="rpz_edit_zonefiles_entry" />
  <br />
  <small><em>click on Save after edit</em></small>
</p>

Multiple adds or edits can be done at one time (before clicking **Apply**)

**Note**: Remember to press **Apply** after you have finished your modifications. The **Apply** sends an `unbound-control reload` which loads the various RPZ configuration files.

<p align="center">
  <img width="800" src="docs/images/rpz_apply.png" alt="rpz_apply" />
  <br />
  <small><em>Do not forget to click Apply</em></small>
</p>


## Custom lists section
List of allowlist domains and blocklist domain.  Loads the custom allow/block list into unbound RPZ. 

<p align="center">
  <img width="800" src="docs/images/rpz_custom_lists.png" alt="rpz_custom_lists" />
  <br />
  <small><em>example custom lists</em></small>
</p>


Domains are entered in this format:
```
domain.com
subdomain.domain.com

# to include all subdomains within a domain, add the "*" to the start of the line
*.domain.com
*.subdomain.domain.com
```

**Note**: the asterisks `*` is only allowed as the first character in the line.   It represents all subdomains within a given domain.

### Allowlist
At times an outside RPZ list will block a needed website. Allowed items can be added to this list and this unblocks that domain.

### Blocklist
The block list operates in a similar way as the allowlist. Make the needed changes to the custom allow/block lists and then click **Save**.

<p align="center">
  <img width="800" src="docs/images/rpz_custom_save2.png" alt="rpz_custom_save" />
  <br />
  <small><em>click on Save after edit</em></small>
</p>

Multiple adds or edits can be done at one time (before clicking **Apply**)

**Note**: Remember to press **Apply** after you have finished your modifications.

<p align="center">
  <img width="800" src="docs/images/rpz_custom_apply2.png" alt="rpz_custom_apply" />
  <br />
  <small><em>click on Apply</em></small>
</p>

##  Logging
RPZ logging can be found in the unbound logs.  Go to **Logs** > **Systems Logs**, then click on **DNS: Unbound** in the drop-down, and then click the **Update** button.

<p align="center">
  <img width="800" src="docs/images/system_log_unbound_rpz.png" alt="system_log_unbound_rpz" />
  <br />
  <small><em>example of RPZ in system logs</em></small>
</p>


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
