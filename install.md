# Install (test version only)

### Send from Mac side to IPFire device
```
iMac:~ jon$ scp -P 222 /Users/jcmurphy/Desktop/rpz-1.0.0-1.ipfire root@ipfire.localdomain:/tmp
#  or
iMac:~ jon$ scp -P 222 /Users/jcmurphy/Desktop/rpz-1.0.0-1.ipfire root@192.168.7.1:/tmp
```

### Send from deb11hpz side to IPFire device to /tmp directory
```
#  go to development folder 
cd /home/jon/development6/ipfire-2.x

#  copy from build environment to ipfire box
scp -P 222 ./packages/rpz-1.0.0-1.ipfire root@ipfire.localdomain:/tmp
```


### install on IPFire side
```
ls -l /tmp

fileName=rpz-1.0.0-1.ipfire

cd /opt/pakfire/tmp/

cp -v "/tmp/${fileName}" /opt/pakfire/tmp

tar xvf "${fileName}"

ls -l /opt/pakfire/tmp

cp -v ROOTFILES /opt/pakfire/db/rootfiles/rpz

NAME=rpz ./install.sh
#  -or-
NAME=rpz ./update.sh

```
