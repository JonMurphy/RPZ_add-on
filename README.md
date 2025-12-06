# Install (test version only)

```
cd /opt/pakfire/tmp

fileName=rpz-beta-0.1.18-18.ipfire.tar

wget https://github.com/JonMurphy/RPZ/raw/refs/heads/main/"${fileName}"

tar xvf "${fileName}"

ls -l /opt/pakfire/tmp

/bin/cp --verbose ROOTFILES /opt/pakfire/db/rootfiles/rpz

NAME=rpz ./install.sh
#  -or-
NAME=rpz ./update.sh

```
