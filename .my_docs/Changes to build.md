Go to:
`cd /home/jon/development6/ipfire-2.x`

#### 1. add new line to `make.sh`
 - add this line to `make.sh` file at `./ipfire-2.x/`

`lfsmake2 rpz`

#### 2. add RPZ menu
 - add to `./ipfire-2.x/config/rootfiles/common/configroot`
 - added alphabetically in this list
 - must include leading `#`

`#var/ipfire/menu.d/EX-rpz.menu`

if missing will generate this message:
```
. . .
vdr (2.6.6)                                                 [        0 ][ DONE ]
bird (2.14)                                                 [        0 ][ DONE ]
Checking Logfiles for new Files
Changes in configroot check rootfile!
*** Build finished in 2:41:47                                           [ DONE ]
jon@deb11HPZ:~
```

#### 3.  add WebGUI page
 - add to `./config/rootfiles/common/web-user-interface`
 - must include leading `#`

`#srv/web/ipfire/cgi-bin/rpz.cgi`


#### 4. add new line to `manualpages` for RPZ wiki
 - add this line to `manualpages` file at `ipfire-2.x/config/cfgroot/manualpages`
 - under the "IPfire menu" section

`rpz.cgi=addons/rpz`


#### 5. add new lines for correct build
 - add to `./ipfire-2.x/config/rootfiles/packages/rpz`

`var/ipfire/menu.d/EX-rpz.menu`

`srv/web/ipfire/cgi-bin/rpz.cgi`
