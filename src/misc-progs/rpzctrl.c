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

int main(int argc, char** argv) {

	char theVersion[] = "2025-01-17 - v08";

	if (!(initsetuid()))
		exit(1);

 	if (argc < 2 || argc > 5) {
		fprintf(stderr, "\nNo argument given.\n");
		fprintf(stderr, "\nrpzctrl list|reload|allowblock|add NAME URL|remove NAME\n");
		fprintf(stderr, "%s\n\n", theVersion);
		exit(1);
	}

    // Do not need name of this program
    // "Shift left" by incrementing argv pointer
    argc--;
    argv++;

	if (strcmp(argv[0], "list") == 0) {
		safe_system("/usr/sbin/rpz-config list");

	} else if (strcmp(argv[0], "reload") == 0) {
		safe_system("/usr/sbin/rpz-config reload");

	} else if (strcmp(argv[0], "restart") == 0) {
		safe_system("/usr/sbin/rpz-config unbound-restart");

	} else if (strcmp(argv[0], "allowblock") == 0) {
		safe_system("/usr/sbin/rpz-make allowblock");

	} else if (strcmp(argv[0], "add") == 0) {
		return run("/usr/sbin/rpz-config", argv);

	} else if (strcmp(argv[0], "remove") == 0) {
		return run("/usr/sbin/rpz-config", argv);

	} else {
		fprintf(stderr, "\nBad argument given.\n");
		fprintf(stderr, "\nrpzctrl list|reload|allowblock|add NAME URL|remove NAME\n");
		fprintf(stderr, "%s\n\n", theVersion);
		exit(1);
	}

	return 0;
}
