# RPZ
RPZ add-on for IPFire


#### Install (test version only)

```
cd /opt/pakfire/tmp/

tar xvf rpz-1.0.0-1.ipfire

ls -l

cp -v ROOTFILES /opt/pakfire/db/rootfiles/rpz

./install.sh

#  Restart unbound to load the recently changed config file

/etc/init.d/unbound restart
```

