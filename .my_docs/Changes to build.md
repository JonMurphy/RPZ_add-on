### For IPFire Build

#### 0. Go to:
```
cd /home/jon/development/ipfire-2.x
```

#### 1. add new line to `make.sh`
 - Edit `./make.sh` and add:

```
lfsmake2 rpz
```
![Screenshot 2024-12-19 at 6 45 12 PM_thumb](https://github.com/user-attachments/assets/8b166af0-9d38-4858-871a-4304b246904f)


#### 2. add RPZ menu
 - Edit `./config/rootfiles/common/configroot` and add:
```
#var/ipfire/menu.d/EX-rpz.menu
```
 - added alphabetically in configroot list
 - must include leading `#`
 - if above is missing `make.sh build` will generate this message:
   ```
    . . .
    vdr (2.6.6)                                                 [        0 ][ DONE ]
    bird (2.14)                                                 [        0 ][ DONE ]
    Checking Logfiles for new Files
    Changes in configroot check rootfile!
    *** Build finished in 2:41:47                                           [ DONE ]
   jon@deb11HPZ:~
    ```
![Screenshot 2024-12-19 at 6 58 51 PM_thumb](https://github.com/user-attachments/assets/67e79f98-5c18-4c98-8403-354c9f3cb384)

#### 3.  add WebGUI page
 - Edit `./config/rootfiles/common/web-user-interface`
 - must include leading `#`
     - maybe because this is an add-on?
```
#srv/web/ipfire/cgi-bin/rpz.cgi
```
![Screenshot 2024-12-19 at 7 14 24 PM_thumb](https://github.com/user-attachments/assets/3cc5c0b3-eed1-4276-9edf-46248df90426)


#### 4. add new line to `manualpages` for RPZ wiki
 - Edit `./config/cfgroot/manualpages` and add:
```
rpz.cgi=addons/rpz
```
 - under the `#  IPfire menu` section

![Screenshot 2024-12-19 at 7 18 45 PM_thumb](https://github.com/user-attachments/assets/f42d6051-ccc7-42fe-8ed5-f1a9a3a2c3a7)



#### 5. add new rootfiles lines for correct build

 - Create an `rpz` file:
 ```
 touch ./config/rootfiles/packages/rpz
 ```
 - Edit `./config/rootfiles/packages/rpz`

```
etc/unbound/local.d/00-rpz.conf
etc/unbound/zonefiles
etc/unbound/zonefiles/allow.rpz
usr/local/bin/rpzctrl
usr/sbin/rpz-config
usr/sbin/rpz-functions
usr/sbin/rpz-make
usr/sbin/rpz-metrics
usr/sbin/rpz-sleep
var/ipfire/addon-lang/rpz.de.pl
var/ipfire/addon-lang/rpz.en.pl
var/ipfire/addon-lang/rpz.es.pl
var/ipfire/addon-lang/rpz.fr.pl
var/ipfire/addon-lang/rpz.it.pl
var/ipfire/addon-lang/rpz.tr.pl
var/ipfire/backup/addons/includes/rpz
var/ipfire/dns/rpz
var/ipfire/dns/rpz/allowlist
var/ipfire/dns/rpz/blocklist
var/ipfire/menu.d/EX-rpz.menu
srv/web/ipfire/cgi-bin/rpz.cgi
```

#### 6. Add rpzctrl
 - edit `./src/misc-progs/Makefile` and add:

```
rpzctrl
```
![Screenshot 2024-12-19 at 7 28 09 PM_thumb](https://github.com/user-attachments/assets/82d739a2-601f-4630-a88b-95bf6da6df51)


#### 7. add to rootfiles
 - edit `./config/rootfiles/common/misc-progs` and add

```
#usr/local/bin/rpzctrl
```
 - must include leading `#`
     - maybe because this is an add-on?
 - added alphabetically in rootfiles list

![Screenshot 2024-12-21 at 10 04 32 PM_thumb](https://github.com/user-attachments/assets/61b1021d-7494-44d2-a972-b06186822d84)
