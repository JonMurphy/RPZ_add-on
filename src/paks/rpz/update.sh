#!/bin/bash
###############################################################################
#                                                                             #
#  IPFire.org - A linux based firewall                                        #
#  Copyright (C) 2024  IPFire Team  <info@ipfire.org>                         #
#                                                                             #
#  This program is free software: you can redistribute it and/or modify       #
#  it under the terms of the GNU General Public License as published by       #
#  the Free Software Foundation, either version 3 of the License, or          #
#  (at your option) any later version.                                        #
#                                                                             #
#  This program is distributed in the hope that it will be useful,            #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#  GNU General Public License for more details.                               #
#                                                                             #
#  You should have received a copy of the GNU General Public License          #
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.      #
#                                                                             #
###############################################################################
#
# Define NAME so functions.sh knows which manifest to use
NAME="rpz"

# Register the manifest in the Pakfire database FIRST
# Logic: Mechanical necessity for future clean uninstalls.
if [ -f "ROOTFILES" ]; then
    cp -pf ROOTFILES /opt/pakfire/db/rootfiles/${NAME}
fi

# shellcheck source=/dev/null
. /opt/pakfire/lib/functions.sh

#  from update.sh
extract_backup_includes

#  stop unbound to delete RPZ conf file
/etc/init.d/unbound stop

#  from uninstall.sh
make_backup ${NAME}
remove_files

#  delete rpz config files.  Otherwise unbound will throw error:
#    "unbound-control[nn:0] error: connect: Connection refused for 127.0.0.1 port 8953"
/bin/rm --verbose --force /etc/unbound/local.d/*.rpz.conf

#  from install.sh
extract_files
restore_backup ${NAME}

# Validate Unbound config before attempting start to avoid DNS blackout.
if /usr/sbin/unbound-checkconf >/dev/null 2>&1; then
    /etc/init.d/unbound start
else
    # Log the failure to system logs
    logger -t "RPZ Update Error: Unbound config invalid. Manual intervention required."
    printf "ERROR: Unbound configuration is invalid! Check /etc/unbound/\n"
fi

#	fix user created files
chown --verbose --recursive nobody:nobody \
	/var/ipfire/dns/rpz    \
	/etc/unbound/zonefiles \
	/etc/unbound/local.d

# Update Language cache
/usr/local/bin/update-lang-cache

#  restart unbound to load config files
/etc/init.d/unbound start
