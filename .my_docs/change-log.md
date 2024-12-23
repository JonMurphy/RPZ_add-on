# Change Log

## rpz-beta-0.1.17-17.ipfire on 2024-12-09
#### rpz-make
 - bug: corrected validation regex for wildcards like: `*.domain.com`


## rpz-beta-0.1.16-16.ipfire on 2024-11-18
#### rpz-make
 - feature: updated validation regex
 - bug: moved validation to beginning of process.  Now we validate before creating config files.

#### rpz.cgi:
 - feature: use CSS color variables of the main ipfire theme
 - bug: empty zonefile remarks were stored as “undef” and caused a warning
 - bug: HTML textarea removes the first empty line in a custom list
 - thank you Leo!


## rpz-beta-0.1.15-15.ipfire on 2024-11-04
#### rpz.cgi:
 - feature: added new language file for Turkish (thank you Peppe)

#### rpz-make
 - bug: corrected empty allow/block list issue.  An empty allow/block list will now remove contents of allow/block.rpz files and remove unneeded allow/block.conf file.  (thank you iptom)


## rpz-beta-0.1.14-14.ipfire on  2024-10-29
#### rpz-config:
 - bug: correct missing rpz extension. `rpz-config list` displayed URL incorrectly (thank you Bernhard)

#### rpz.cgi:
 - bug: remove extra `"` in language files (thank you Bernhard)
 - feature: slightly dim "apply" button when not enabled


## rpz-beta-0.1.13-13.ipfire on 2024-10-27
 - skipped (error in change to config script)


## rpz-beta-0.1.12-12.ipfire on 2024-10-21
#### rpz.cgi:
 - feature: added new language file for French  (thank you gw-ipfire)


## rpz-beta-0.1.11-11.ipfire on 2024-10-18
#### rpz.cgi:
- feature: added new language file for Italian (thank you umberto)
- feature: added new language file for Spanish (thank you Roberto)


## rpz-beta-0.1.10-10.ipfire on 2024-10-15
#### rpz-make:
 - bug: corrected validation error for a custom list entry (thank you siosios)
 - e.g., `*.cloudflare-dns.com`
#### install.sh:
 - bug: add chown to correct user created files

#### update.sh:
 - bug: add chown to correct user created files (thank you siosios)


## rpz-beta-0.1.9-9.ipfire on 2024-10-08
#### rpz.cgi:
 - feature: added new language file for German (thank you Leo)
 - bug: add missing "rpz exitcode 110"
 - bug: corrected missing RPZ menu item at menu > IPFire


## rpz-beta-0.1.8-8.ipfire on 2024-10-04
 - skipped (error in change to install.sh file)


## rpz-beta-0.1.7-7.ipfire on 2024-10-03
#### All:
 - update: includes beta version numbers for pakfire package, instead of only `rpz-1.0.0-1.ipfire`, for each release.

#### rpz.cgi:
 - feature: added new WebGUI at `rpz.cgi`
    - a BIG thank you to Leo Hofmann for all of his work creating the webgui!!
 - bug: corrected missing RPZ menu item at menu > IPFire

#### rpz-make:
 - feature: validate entries in allowlist and blocklist
 - feature: add "no-reload" option for WebGUI

#### rpz-metrics:
 - feature: info can be sorted by name, by hit count, by line count, by "enabled" list or all lists

#### backups:
 - bug: include all files in `/var/ipfire/dns/rpz` directory in backup

#### update.sh:
 - bug: corrected ownership for `/var/ipfire/dns/rpz` directory during an update

#### Build:
 - remove `block.rpz.conf` and `block.rpz` from build.  Files to be created by `rpz-make`
