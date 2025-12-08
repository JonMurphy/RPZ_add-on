# Using the RPZ Console

All of the RPZ console commands on one page!


## Usage via Console/Terminal
To run this add-on, open the serial console, or open the local terminal, to access the IPFire box via SSH.  There are four simple scripts available for set-up:

[rpz-config](rpz#create-a-config-file-for-rpz-via-rpz-config) - Create or remove an external RPZ file

[rpz-make](rpz#custom-allow-list-or-block-list-via-rpz-make) - Loads custom allow lists and blocks lists into unbound RPZ

[rpz-metrics](rpz#metrics-of-rpz-usage-via-rpz-metrics) - Locates RPZ names from the message logs and sort by name.

[rpz-sleep](rpz#pause-rpz-for-n-time-via-rpz-sleep) - Pause RPZ for a NUMBER of seconds (default 5 minutes).


## Create a config file for RPZ via "rpz-config"
The `rpz-config` script assists in creating or deleting RPZ files.

```bash
Usage: 	rpz-config  <action> <name> <url> <option>
		create or delete RPZ configuration files

Actions:
  add <name> <url>	adds new RPZ config file by RPZ name
  remove <name>		removes unneeded RPZ files by RPZ name
    <name>             unique alpha-numeric name for the RPZ file.  This name appears in the message log and
                         is the base file name for the config file. e.g., threatfox, urlhaus, PopUpAdsHZ
    <url>              URL for RPZ.  Must be in a format similar to https://example.com/path/filename.
                         Other protocols such as file://, ftp://, etc., will not work.
  reload            reloads configuration into unbound 
  list              lists all active RPZ names and URLs
```
<br>
Example commands:

```bash
rpz-config add MxLightHZ https://raw.githubusercontent.com/hagezi/dns-blocklists/main/rpz/light.txt

rpz-config remove MxLightHZ
```

IMAGE

![](docs/images/rpz-config.png "example rpz-config command")

<p align="center">
  <img width="780" src="docs/images/rpz-config.png" alt="rpz-config" />
  <br />
  <small><em>example rpz-config command</em></small>
  <br />
</p>

## Custom allow list or block list via "rpz-make"
The `rpz-make` script loads the custom allow/block list into unbound RPZ.

```bash
Usage:    rpz-make <name>
            build the custom allow or block RPZ files
Name:
  allow       build RPZ file from allowlist
  block       build RPZ file from blocklist
  allowblock  build both RPZ files
  reload      reloads configuration into unbound
```

Example commands:
```bash
rpz-make allow
rpz-make block
rpz-make allowblock
```

### Allow list
Sometimes outside RPZ lists will block a needed website.  Allowed items can be added to this list.

Edit the `/var/ipfire/dns/rpz/allowlist` and add the needed websites:

IMAGE

![](docs/images/rpz_allow.png "example allowlist")

<p align="center">
  <img width="780" src="docs/images/rpz_allow.png" alt="rpz_allow" />
  <br />
  <small><em>example allowlist</em></small>
  <br />
</p>

### Block list
The block list operates in a similar way as the allow list and is located at `/var/ipfire/dns/rpz/blocklist`:

IMAGE

![](docs/images/rpz_block.png "example blocklist")

<p align="center">
  <img width="780" src="docs/images/rpz_block.png" alt="rpz_block" />
  <br />
  <small><em>example blocklist</em></small>
  <br />
</p>

## Metrics of RPZ usage via "rpz-metrics"
The `rpz-metrics` script searches the message logs for RPZ names and sorts the result (default sort is NAME).  Selecting all message logs (1 year or 53 message log files) may take ~60 seconds to complete.

```bash
Usage: 	rpz-metrics <number of message logs> <option>
    default <number of message logs> is 2
    default <option> is sort by NAME

Option to sort:
  --by-name		sort the results by name

  --by-hits		sort the results by number of hits

  --by-lines	sort the results by number of lines in a RPZ list

  --active-all	include enabled lists and disabled list in results
```

IMAGE

![](docs/images/rpz_metrics.png "example metrics")

<p align="center">
  <img width="780" src="docs/images/rpz_metrics.png" alt="rpz_metrics" />
  <br />
  <small><em>example metrics</em></small>
  <br />
</p>

### Pause RPZ for N time via "rpz-sleep"
Pause for NUMBER seconds. SUFFIX may be 's' for seconds, 'm' for minutes, 'h' for hours or 'd' for days.

```bash
Usage: 	rpz-sleep <sleep time>
    default <sleep time> is 5 minutes
```

IMAGE

![](docs/images/rpz_sleep.png "example sleep rpz")

<p align="center">
  <img width="780" src="docs/images/rpz-config.png" alt="rpz-config" />
  <br />
  <small><em>example rpz-config command</em></small>
  <br />
</p>

##  Logging
RPZ logging can be found in the unbound logs.  Go to **Logs** > **Systems Logs**, then click on **DNS: Unbound** in the drop-down, and then click the **Update** button.

IMAGE

![](docs/images/system_log_unbound_rpz.png "example of RPZ in system logs")

<p align="center">
  <img width="780" src="docs/images/rpz-config.png" alt="rpz-config" />
  <br />
  <small><em>example rpz-config command</em></small>
  <br />
</p>

### Notes
 1. Large RPZ files will slow down the unbound reload time and slow down a DNS lookup.  Over 500,000 lines of RPZ files (total lines for all RPZ files) is discouraged. Over 1,000,000 lines of RPZ files (total lines for all RPZ files) is NOT recommended.
    - the Hagezi Threat Intelligence Feed (largest size) is **NOT** recommended due to it's large size (lines = 1,354,431)
        - Hagezi TIF medium or TIF mini should be fine.
    - the Hagezi Gambling (largest size) is **NOT** recommended due to it's large size (lines = 937,035)
        - Hagezi Gambling medium or Gambling mini should be fine.
 3. Keep in mind there may be overlap between an RPZ list and a list offered in [IP Address Blocklists](https://www.ipfire.org/docs/configuration/firewall/ipblocklist).  Please review the lists chosen before activating.


[^1]: [https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html](https://unbound.docs.nlnetlabs.nl/en/latest/topics/filtering/rpz.html)
[^2]: [https://jpgpi250.github.io/piholemanual/doc/Unbound%20response%20policy%20zones.pdf](https://jpgpi250.github.io/piholemanual/doc/Unbound%20response%20policy%20zones.pdf)
