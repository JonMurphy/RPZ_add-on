/* This file is part of the IPFire Firewall.
 *
 * This program is distributed under the terms of the GNU General Public
 * Licence.  See the file COPYING for details.
 *
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include "setuid.h"

int main(int argc, char *argv[]) {

	if (!(initsetuid()))
		exit(1);

	if (argc < 2) {
		fprintf(stderr, "\nNo argument given.\n\nrpzctrl list|reload|allowblock|add NAME|remove NAME\n\n");
		exit(1);
	}

	if (strcmp(argv[1], "list") == 0) {
		system_output('/usr/sbin/rpz-config', 'list');

	} else if (strcmp(argv[1], "reload") == 0) {
		safe_system('/usr/sbin/rpz-config', 'reload');

	} else if (strcmp(argv[1], "allowblock") == 0) {
		safe_system('/usr/sbin/rpz-make', 'allowblock', '--no-reload');

	} else if (strcmp(argv[1], "add") == 0) {
		safe_system('/usr/sbin/rpz-config', 'add', strcmp(argv[2], '--no-reload');

	} else if (strcmp(argv[1], "remove") == 0) {
		safe_system('/usr/sbin/rpz-config', 'remove', strcmp(argv[2], '--no-reload');

	} else {
		fprintf(stderr, "\nBad argument given.\n\nrpzctrl list|reload|allowblock|add NAME|remove NAME\n\n");
		exit(1);
	}

	return 0;
}
