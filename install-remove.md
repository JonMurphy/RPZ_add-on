# Install (test version only)

### Mac side
```
iMac:~ jon$ scp -P 222 /Users/jcmurphy/Desktop/rpz-1.0.0-1.ipfire root@ipfire.localdomain:/tmp
#  or
iMac:~ jon$ scp -P 222 /Users/jcmurphy/Desktop/rpz-1.0.0-1.ipfire root@192.168.7.1:/tmp

#
ssh -p 222 root@ipfire.localdomain
#  or
ssh -p 222 root@192.168.7.1
```

### IPFire side
```
ls -l /tmp

cd /opt/pakfire/tmp/

cp -v /tmp/rpz-1.0.0-1.ipfire /opt/pakfire/tmp

tar xvf rpz-1.0.0-1.ipfire

ls -l /opt/pakfire/tmp

cp -v ROOTFILES /opt/pakfire/db/rootfiles/rpz

NAME=rpz ./install.sh
```
