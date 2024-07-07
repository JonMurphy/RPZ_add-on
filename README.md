# RPZ
RPZ add-on for IPFire


#### Install (test version only)

### Mac side
```
iMac:~ jon$ scp -P 222 /Users/jcmurphy/Desktop/rpz-1.0.0-1.ipfire root@ipfire.localdomain:/tmp
#  or
iMac:~ jon$ scp -P 222 /Users/jcmurphy/Desktop/rpz-1.0.0-1.ipfire root@192.168.7.1:/tmp
```

### IPFire side
```
ls -l /tmp

cd /opt/pakfire/tmp/

cp -v /tmp/*.ipfire /opt/pakfire/tmp

tar xvf rpz-1.0.0-1.ipfire

ls -l /opt/pakfire/tmp

cp -v ROOTFILES /opt/pakfire/db/rootfiles/rpz

NAME=rpz ./install.sh

#  Restart unbound to load the recently changed config file

/etc/init.d/unbound restart
```

