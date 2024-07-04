# RPZ

RPZ is a 

## Installation
rpz can be installed with the Pakfire web interface or via the console:

```bash
pakfire install rpz
```

## Usage
There is no web interface for this Addon. To run this Addon open the client console or terminal and access the IPFire box via SSH.

There are four simple scripts

rpzAllowBlock
rpzConfig
rpzMetrics
rpzSleep


## Custom allow list or block list

Usage: 	rpzAllowBlock
  Loads the allow and blocks lists into unbound RPZ





## Create a config file for RPZ

```
Usage: 	rpzConfig.sh  [options] <name>  <url>
  Assists in creating, removing or replacing an RPZ config file

Options:
--add <name> <url>   adds new RPZ config file by RPZ name

--remove <name>      removes unneeded RPZ files by RPZ name

--replace <name>     replaces an existing RPZ files with a new config file

<name>               unique alpha-numeric name for the RPZ file.
                       This name appears in the message log and
                       is the basename for the config file. e.g., threatfox, urlhaus, PopUpAdsHZ

<url>                URL for RPZ.  Must be in a format similar to
                       https://example.com/path/filename.  Other protocols such
                       as file://, ftp://, etc. will not work.
```

**Note**: whenever a RPZ config file is added, removed, or replaced, the upbound reload (i.e., `unbound-control reload`) is run.  This loads all of the new settings.  Keep in mind this may pause DNS up to ~60 seconds depending on the size of the RPZ files.  Large RPZ files will slow down the unbound reload time.







### Example: Local backup of IPFire device

 1. Format (as ext4) and mount an external drive.  See [](/configuration/services/extrahd)
     * Example:  mount point of `/mnt/hdd`
 2. Create a new directory for the repository
     * Example:  `mkdir --verbose --mode=777 /mnt/hdd/rsnapshot`
     * this is **snapshot_root** from the `/etc/rsnapshot.conf` file
 3. Make your changes to the `/etc/rsnapshot.conf` file.
 4. Run this command to check the `/etc/rsnapshot.conf` file:
```bash
$ rsnapshot configtest
```
 5a. Make changes to fcron.hourly, fcron.daily, fcron.weekly, fcron.monthly:

```bash
ln -vs /var/ipfire/backup/bin/rsnapshot-hourly /etc/fcron.hourly
ln -vs /var/ipfire/backup/bin/rsnapshot-daily /etc/fcron.daily
ln -vs /var/ipfire/backup/bin/rsnapshot-weekly /etc/fcron.weekly
ln -vs /var/ipfire/backup/bin/rsnapshot-monthly /etc/fcron.monthly
```
**-or-**

 5b. Make changes to fcrontab:

```bash
# m h  dom mon dow   command
30 * * * *	/usr/bin/rsnapshot sync 2>&1 && /usr/bin/rsnapshot hourly 2>&1
20 0 * * *	/usr/bin/rsnapshot daily 2>&1
15 0 * * 0	/usr/bin/rsnapshot weekly 2>&1
10 0 1 * *	/usr/bin/rsnapshot monthly 2>&1
05 0 1 1 *	/usr/bin/rsnapshot yearly 2>&1
```

## Links
 * [rsnapshot home page](https://rsnapshot.org)
 * [HowTo for rsnapshot](https://wiki.ipfire.org/addons/rsnapshot/rsnapshot_howto.en.html)
 * [github - rsnapshot](https://github.com/rsnapshot/rsnapshot)


[^1]: Introduction from <https://rsnapshot.org>
