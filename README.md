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
cd /opt/pakfire/tmp/

cp -v cp /tmp/*.ipfire /opt/pakfire/tmp

tar xvf rpz-1.0.0-1.ipfire

ls -l

cp -v ROOTFILES /opt/pakfire/db/rootfiles/rpz

./install.sh

#  Restart unbound to load the recently changed config file

/etc/init.d/unbound restart
```

