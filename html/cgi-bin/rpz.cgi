#!/usr/bin/perl
###############################################################################
#                                                                             #
# IPFire.org - A linux based firewall                                         #
# Copyright (C) 2005-2024  IPFire Team  <info@ipfire.org>                     #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU General Public License as published by        #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
#                                                                             #
###############################################################################

use strict;
use Scalar::Util qw(looks_like_number);

# debugging
#use warnings;
#use CGI::Carp 'fatalsToBrowser';
#use Data::Dumper;

require '/var/ipfire/general-functions.pl';
require "${General::swroot}/lang.pl";
require "${General::swroot}/header.pl";

###--- Extra HTML ---###
my $extraHead = <<END
<style>
	/* alternating row background color */
	.tbl tr:nth-child(2n+2) {
		background-color: #f0f0f0;
	}
	.tbl tr:nth-child(2n+3) {
		background-color: #d6d6d6;
	}
	/* text alignment */
	.tbl th:not(:last-child) {
		text-align: left;
	}
	div.right {
		text-align: right;
		margin-top: 0.5em;
	}
	textarea.domainlist {
		margin: 0.5em 0;
		resize: vertical;
		min-height: 10em;
		overflow: auto;
		white-space: pre;
	}
</style>
END
;
###--- End of extra HTML ---###


### Settings ###

# Request DNS service reload after configuration change
my $RPZ_RELOAD_FLAG = "${General::swroot}/dns/rpz/reload.flag";

# Configuration file for all available zonefiles
# Format: index, name (unique), enabled (on/off), URL, remark
my $ZONEFILES_CONF = "${General::swroot}/dns/rpz/zonefiles.conf";

# Configuration file for custom lists
# IDs: 0=allowlist, 1=blocklist, 2=options (allow/block enabled)
my $CUSTOMLISTS_CONF = "${General::swroot}/dns/rpz/customlists.conf";

# Export custom lists to rpz-config
my $RPZ_ALLOWLIST = "${General::swroot}/dns/rpz/allowlist";
my $RPZ_BLOCKLIST = "${General::swroot}/dns/rpz/blocklist";


### Preparation ###

# Create missing config files
unless(-f $ZONEFILES_CONF) { &General::safe_system('touch', "$ZONEFILES_CONF"); }
unless(-f $CUSTOMLISTS_CONF) { &General::safe_system('touch', "$CUSTOMLISTS_CONF"); }


## Global gui variables
my $errormessage = "";

## Global configuration data
my %zonefiles = ();
my %customlists = ();
&_zonefiles_load();
&_customlists_load();

## Global CGI form data
my %cgiparams = ();
&Header::getcgihash(\%cgiparams);

my $action = $cgiparams{'ACTION'} // 'NONE';
my $action_key = $cgiparams{'KEY'} // ''; # entry being edited, empty = none/new


###--- Process form actions ---###

# Zonefiles action: Check whether the requested entry exists
if((substr($action, 0, 3) eq 'ZF_') && ($action_key)) {
	unless(defined $zonefiles{$action_key}) {
		$errormessage = &_rpz_error_tr(204, $action_key);
		$action = 'NONE';
	}
}

## Perform actions
if($action eq 'ZF_SAVE') {				## Save new or modified zonefiles entry
	if(&_action_zf_save()) {
		$action = 'NONE'; # success, return to main page
		&_http_prg_redirect();
	} else {
		$action = 'ZF_EDIT'; # error occured, keep editing
	}

} elsif($action eq 'ZF_TOGGLE') {		## Toggle on/off
	if(&_action_zf_toggle()) {
		$action = 'NONE';
		&_http_prg_redirect();
	}

} elsif($action eq 'ZF_REMOVE') {		## Remove entry
	if(&_action_zf_remove()) {
		$action = 'NONE';
		&_http_prg_redirect();
	}

} elsif($action eq 'CL_SAVE') {			## Save custom lists
	if(&_action_cl_save()) {
		$action = 'NONE';
		&_http_prg_redirect();
	}

} elsif($action eq 'RPZ_RELOAD') {		## Reload dns service
	if(&_action_rpz_reload()) {
		$action = 'NONE';
		&_http_prg_redirect();
	}

}


###--- Start GUI ---###

## Start http output
&Header::showhttpheaders();

# Start HTML
&Header::openpage($Lang::tr{'rpz'}, 1, $extraHead);
&Header::openbigbox('100%', 'left', '');

# Show error messages
if($errormessage) {
	&_print_message($errormessage);
}

# Handle zonefile add/edit mode
if($action eq "ZF_EDIT") {
	&_print_zonefile_editor();

	# Finalize page and exit cleanly
	&Header::closebigbox();
	&Header::closepage();
	exit(0);
}

# Show gui elements
&_print_zonefiles();
&_print_customlists();

&Header::closebigbox();
&Header::closepage();

###--- End of GUI ---###


###--- Internal configuration file functions ---###

# Load all available zonefiles from rpz-config and the internal configuration
sub _zonefiles_load {
	# Clean start
	%zonefiles = ();

	# Source 1: Get the currently enabled zonefiles from rpz-config (expected format [URL]=[remark])
	my @enabled_files = &General::system_output('/usr/sbin/rpz-config', 'list');

	foreach my $row (@enabled_files) {
		chomp($row);

		# Use regex instead of split() to skip non-matching lines
		next unless($row =~ /^(\w+)=(.+)$/);
		my ($name, $url) = ($1, $2);

		# Unique names are already guaranteed by rpz-config
		if(&_rpz_validate_zonefile($name, $url, '', 0) == 0) {
			# Populate global data hash, mark all found entries as enabled
			my %entry = ('enabled' => 'on', 'url' => $url, 'remark' => $Lang::tr{'rpz zf imported'});
			$zonefiles{$name} = \%entry;
		}
	}

	# Source 2: Get additional data and disabled entries from configuration file
	my %configured_files = ();
	&General::readhasharray($ZONEFILES_CONF, \%configured_files);

	foreach my $row (values (%configured_files)) {
		my ($name, $enabled, $url, $remark) = @$row;
		next unless($name);

		# Check whether this row belongs to an entry already imported from rpz-config
		if(defined $zonefiles{$name}) {
			# Existing entry, only merge additional data
			$zonefiles{$name}{'remark'} = $remark;
		} else {
			# Skip entry if it is marked as enabled but not found by rpz-config. It was then deleted manually
			if($enabled ne 'on') {
				# Populate global data hash
				my %entry = ('enabled' => 'off', 'url' => $url, 'remark' => $remark);
				$zonefiles{$name} = \%entry;
			}
		}
	}
}

# Save internal zonefiles configuration
sub _zonefiles_save_conf {
	my $index = 0;
	my %export = ();

	# Loop trough all zonefiles and create "hasharray" type export
	foreach my $name (keys %zonefiles) {
		my @entry = ($name,
			$zonefiles{$name}{'enabled'},
			$zonefiles{$name}{'url'},
			$zonefiles{$name}{'remark'});

		$export{$index++} = \@entry;
	}

	&General::writehasharray($ZONEFILES_CONF, \%export);
}

# Load custom lists from rpz-config and the internal configuration
sub _customlists_load {
	# Clean start
	%customlists = ();

	# Load configuration file
	my %lists_conf = ();
	&General::readhasharray($CUSTOMLISTS_CONF, \%lists_conf);

	# Get list options, enabled by default to start import
	$customlists{'allow'}{'enabled'} = $lists_conf{2}[0] // 'on';
	$customlists{'block'}{'enabled'} = $lists_conf{2}[1] // 'on';

	# Import enabled list from rpz-config, otherwise retrieve stored or empty list from configuration file
	if($customlists{'allow'}{'enabled'} eq 'on') {
		&_customlist_import('allow', $RPZ_ALLOWLIST);
	} else {
		$customlists{'allow'}{'list'} = $lists_conf{0} // [];
	}
	if($customlists{'block'}{'enabled'} eq 'on') {
		&_customlist_import('block', $RPZ_BLOCKLIST);
	} else {
		$customlists{'block'}{'list'} = $lists_conf{1} // [];
	}
}

# Save internal custom lists configuration
sub _customlists_save_conf {
	my %export = ();

	# Match IDs with import function
	$export{0} = $customlists{'allow'}{'list'};
	$export{1} = $customlists{'block'}{'list'};
	$export{2} = [$customlists{'allow'}{'enabled'}, $customlists{'block'}{'enabled'}];

	&General::writehasharray($CUSTOMLISTS_CONF, \%export);
}

# Import a custom list from plain file, returns empty list if file is missing
sub _customlist_import {
	my ($listname, $filename) = @_;
	my @list = ();

	# File exists, load and check all lines
	if(-f $filename) {
		open(my $FH, '<', $filename) or die "Can't read $filename: $!";
		while(my $line = <$FH>) {
			chomp($line);
			push(@list, $line);
		}
		close($FH);

		# Clean up imported data
		&_rpz_validate_customlist(\@list, 1);
	}

	$customlists{$listname}{'list'} = \@list;
}

# Export a custom list to plain file or clear file if list is disabled
sub _customlist_export {
	my ($listname, $filename) = @_;
	return unless(defined $customlists{$listname});

	# Write enabled domain list to file, otherwise save empty file
	open(my $FH, '>', $filename) or die "Can't write $filename: $!";

	if($customlists{$listname}{'enabled'} eq 'on') {
		foreach my $line (@{$customlists{$listname}{'list'}}) {
			print $FH "$line\n";
		}
	} else {
		print $FH "; Note: This list is currently disabled by $ENV{'SCRIPT_NAME'}\n";
	}

	close($FH);
}


###--- Internal gui functions ---###

# Show simple message box
sub _print_message {
	my ($message, $title) = @_;
	$title ||= $Lang::tr{'error messages'};

	&Header::openbox('100%', 'left', $title);
	print "<span>$message</span>";
	&Header::closebox();
}

# Show all zone files and related gui elements
sub _print_zonefiles {
	&Header::openbox('100%', 'left', $Lang::tr{'rpz zf'});

	print <<END
<table class="tbl" width="100%">
	<tr>
		<th>$Lang::tr{'name'}</th>
		<th>URL</th>
		<th>$Lang::tr{'remark'}</th>
		<th colspan="3">$Lang::tr{'action'}</th>
	</tr>
END
;

	# Sort zonefiles by name and loop trough all entries
	foreach my $name (sort keys %zonefiles) {

		# Toggle button label translation
		my $toggle_tr = ($zonefiles{$name}{'enabled'} eq 'on') ? $Lang::tr{'click to disable'} : $Lang::tr{'click to enable'};

		print <<END
	<tr>
		<td>$name</td>
		<td>$zonefiles{$name}{'url'}</td>
		<td>$zonefiles{$name}{'remark'}</td>

		<td align="center" width="5%">
			<form method="post" action="$ENV{'SCRIPT_NAME'}">
				<input type="hidden" name="KEY" value="$name">
				<input type="hidden" name="ACTION" value="ZF_TOGGLE">
				<input type="image" src="/images/$zonefiles{$name}{'enabled'}.gif" title="$toggle_tr" alt="$toggle_tr">
			</form>
		</td>
		<td align="center" width="5%">
			<form method="post" action="$ENV{'SCRIPT_NAME'}">
				<input type="hidden" name="KEY" value="$name">
				<input type="hidden" name="ACTION" value="ZF_EDIT">
				<input type="image" src="/images/edit.gif" title="$Lang::tr{'edit'}" alt="$Lang::tr{'edit'}">
			</form>
		</td>
		<td align="center" width="5%">
			<form method="post" action="$ENV{'SCRIPT_NAME'}">
				<input type="hidden" name="KEY" value="$name">
				<input type="hidden" name="ACTION" value="ZF_REMOVE">
				<input type="image" src="/images/delete.gif" title="$Lang::tr{'remove'}" alt="$Lang::tr{'remove'}">
			</form>
		</td>
	</tr>
END
;
	}

	# Disable reload button if not needed
	my $reload_state = &_rpz_needs_reload() ? "" : " disabled";

	print <<END
</table>

<div class="right">
	<form method="post" action="$ENV{'SCRIPT_NAME'}">
		<input type="hidden" name="KEY" value="">
		<button type="submit" name="ACTION" value="ZF_EDIT">$Lang::tr{'add'}</button>
		<button type="submit" name="ACTION" value="RPZ_RELOAD"$reload_state>$Lang::tr{'update'}</button>
	</form>
</div>
END
;

	&Header::closebox();
}

# Show zonefiles entry editor
sub _print_zonefile_editor {

	# Key specified: Edit existing entry
	if(($action_key) && (defined $zonefiles{$action_key})) {
		# Load data to be edited, but don't override already present values (allows user to edit after error)
		$cgiparams{'ZF_NAME'} //= $action_key;
		$cgiparams{'ZF_URL'} //= $zonefiles{$action_key}{'url'};
		$cgiparams{'ZF_REMARK'} //= $zonefiles{$action_key}{'remark'};
	}

	# Fallback to empty form
	$cgiparams{'ZF_NAME'} //= "";
	$cgiparams{'ZF_URL'} //= "";
	$cgiparams{'ZF_REMARK'} //= "";

	&Header::openbox('100%', 'left', $Lang::tr{'rpz zf editor'});

	print <<END
<form method="post" action="$ENV{'SCRIPT_NAME'}">
<input type="hidden" name="KEY" value="$action_key">
<table width="100%">
	<tr>
		<td width="20%">$Lang::tr{'name'}:&nbsp;<img src="/blob.gif" alt="*"></td>
		<td><input type="text" name="ZF_NAME" value="$cgiparams{'ZF_NAME'}" size="40" maxlength="32" title="$Lang::tr{'rpz zf remark info'}" pattern="[a-zA-Z0-9_]{1,32}" required></td>
	</tr>
	<tr>
		<td width="20%">URL:&nbsp;<img src="/blob.gif" alt="*"></td>
		<td><input type="url" name="ZF_URL" value="$cgiparams{'ZF_URL'}" size="40" maxlength="128" required></td>
	</tr>
	<tr>
		<td width="20%">$Lang::tr{'remark'}:</td>
		<td><input type="text" name="ZF_REMARK" value="$cgiparams{'ZF_REMARK'}" size="40" maxlength="32"></td>
	</tr>
	<tr>
		<td colspan="2"><hr></td>
	</tr>
	<tr>
		<td width="55%"><img src="/blob.gif" alt="*">&nbsp;$Lang::tr{'required field'}</td>
		<td align="right"><button type="submit" name="ACTION" value="ZF_SAVE">$Lang::tr{'save'}</button></td>
	</tr>
</table>
</form>

<div class="right">
	<form method="post" action="$ENV{'SCRIPT_NAME'}">
		<button type="submit" name="ACTION" value="NONE">$Lang::tr{'back'}</button>
	</form>
</div>
END
;

	&Header::closebox();
}

# Show custom allow/block files and related gui elements
sub _print_customlists {

	# Load lists from config, unless they are currently being edited
	if($action ne 'CL_SAVE') {
		$cgiparams{'ALLOW_LIST'} = join("\n", @{$customlists{'allow'}{'list'}});
		$cgiparams{'BLOCK_LIST'} = join("\n", @{$customlists{'block'}{'list'}});

		$cgiparams{'ALLOW_ENABLED'} = ($customlists{'allow'}{'enabled'} eq 'on') ? 'on' : undef;
		$cgiparams{'BLOCK_ENABLED'} = ($customlists{'block'}{'enabled'} eq 'on') ? 'on' : undef;
	}

	# Fallback to empty form
	$cgiparams{'ALLOW_LIST'} //= "";
	$cgiparams{'BLOCK_LIST'} //= "";

	# HTML checkboxes, unchecked = no or undef value in POST data
	my %checked = ();
	$checked{'ALLOW_ENABLED'} = (defined $cgiparams{'ALLOW_ENABLED'}) ? " checked" : "";
	$checked{'BLOCK_ENABLED'} = (defined $cgiparams{'BLOCK_ENABLED'}) ? " checked" : "";

	# Disable reload button if not needed
	my $reload_state = &_rpz_needs_reload() ? "" : " disabled";

	&Header::openbox('100%', 'left', $Lang::tr{'rpz cl'});

	print <<END
<form method="post" action="$ENV{'SCRIPT_NAME'}">
<table width="100%">
	<tr>
		<td colspan="2"><b>$Lang::tr{'rpz cl allow'}</b><br>$Lang::tr{'rpz cl allow info'}</td>
		<td colspan="2"><b>$Lang::tr{'rpz cl block'}</b><br>$Lang::tr{'rpz cl block info'}</td>
	</tr>
	<tr>
		<td colspan="2"><textarea name="ALLOW_LIST" class="domainlist" cols="45">$cgiparams{'ALLOW_LIST'}</textarea></td>
		<td colspan="2"><textarea name="BLOCK_LIST" class="domainlist" cols="45">$cgiparams{'BLOCK_LIST'}</textarea></td>
	</tr>
	<tr>
		<td><label for="allow_enabled">$Lang::tr{'rpz cl allow enable'}</label></td>
		<td width="15%"><input type="checkbox" name="ALLOW_ENABLED" id="allow_enabled"$checked{'ALLOW_ENABLED'}></td>
		<td><label for="block_enabled">$Lang::tr{'rpz cl block enable'}</label></td>
		<td width="15%"><input type="checkbox" name="BLOCK_ENABLED" id="block_enabled"$checked{'BLOCK_ENABLED'}></td>
	</tr>
	<tr>
		<td colspan="4"><hr></td>
	</tr>
	<tr>
		<td align="right" colspan="4">
			<button type="submit" name="ACTION" value="CL_SAVE">$Lang::tr{'save'}</button>
			<button type="submit" name="ACTION" value="RPZ_RELOAD"$reload_state>$Lang::tr{'update'}</button>
		</td>
</table>
</form>
END
;

	&Header::closebox();
}


###--- Internal action processing functions ---###

# Toggle zonefile on/off
sub _action_zf_toggle {
	return unless(defined $zonefiles{$action_key});

	my $result = 0;
	my $enabled = $zonefiles{$action_key}{'enabled'};

	# Perform toggle action
	if($enabled eq 'on') {
		$enabled = 'off';
		$result = &General::system('/usr/sbin/rpz-config', 'remove', $action_key, '--no-reload');
	} else {
		$enabled = 'on';
		$result = &General::system('/usr/sbin/rpz-config', 'add', $action_key, $zonefiles{$action_key}{'url'}, '--no-reload');
	}

	# Check for errors, request service reload on success
	return unless &_rpz_check_result($result, 1);

	# Save changes
	$zonefiles{$action_key}{'enabled'} = $enabled;
	&_zonefiles_save_conf();

	return 1;
}

# Remove zonefile
sub _action_zf_remove {
	return unless(defined $zonefiles{$action_key});

	# Remove from rpz-config if currently active
	if($zonefiles{$action_key}{'enabled'} eq 'on') {
		my $result = &General::system('/usr/sbin/rpz-config', 'remove', $action_key, '--no-reload');

		# Check for errors, request service reload on success
		return unless &_rpz_check_result($result, 1);
	}

	# Remove from data hash and save changes
	delete $zonefiles{$action_key};
	&_zonefiles_save_conf();

	# Clear action_key, as the entry is now removed entirely
	$action_key = "";

	return 1;
}

# Create or update zonefile entry
# Returns undef if gui needs to stay in editor mode
sub _action_zf_save {
	my $result = 0;

	my $name = $cgiparams{'ZF_NAME'} // "";
	my $url = $cgiparams{'ZF_URL'} // "";
	my $remark = $cgiparams{'ZF_REMARK'} // "";
	my $enabled = 'on'; # Enable new entries by default

	# Note on variables:
	# name = unique key, will be used to address the entry
	# action_key = name of the entry being edited, empty for new entry

	# Only check for unique name if it changed
	# (this also checks new entries because the action_key is empty in this case)
	$result = &_rpz_validate_zonefile($name, $url, $remark, (lc($name) ne lc($action_key)));
	return unless &_rpz_check_result($result, 0);

	# Edit existing entry: Determine what was changed
	if(($action_key) && (defined $zonefiles{$action_key})) {
		# Name und URL remain unchanged, only save remark and finish
		if(($name eq $action_key) && ($url eq $zonefiles{$action_key}{'url'})) {
			$zonefiles{$action_key}{'remark'} = $remark;
			&_zonefiles_save_conf();

			return 1;
		}

		# Entry was changed and needs to be recreated, preserve status
		$enabled = $zonefiles{$action_key}{'enabled'};

		# Remove from rpz-config
		return unless &_action_zf_remove();
	}

	# Add new entry to rpz-config
	if($enabled eq 'on') {
		$result = &General::system('/usr/sbin/rpz-config', 'add', $name, $url, '--no-reload');

		# Check for errors, request service reload on success
		return unless &_rpz_check_result($result, 1);
	}

	# Add to global data hash and save changes
	my %entry = ('enabled' => $enabled, 'url' => $url, 'remark' => $remark);
	$zonefiles{$name} = \%entry;
	&_zonefiles_save_conf();

	return 1;
}

# Save custom lists
sub _action_cl_save {
	return unless((defined $cgiparams{'ALLOW_LIST'}) && (defined $cgiparams{'BLOCK_LIST'}));

	my $result = 0;

	my @allowlist = split(/\R/, $cgiparams{'ALLOW_LIST'});
	my @blocklist = split(/\R/, $cgiparams{'BLOCK_LIST'});

	# Validate lists
	$result = &_rpz_validate_customlist(\@allowlist);
	if($result != 0) {
		$errormessage = &_rpz_error_tr(202, $result);
		return;
	}
	$result = &_rpz_validate_customlist(\@blocklist);
	if($result != 0) {
		$errormessage = &_rpz_error_tr(203, $result);
		return;
	}

	# Add to global data hash and save changes
	$customlists{'allow'}{'list'} = \@allowlist;
	$customlists{'block'}{'list'} = \@blocklist;
	$customlists{'allow'}{'enabled'} = (defined $cgiparams{'ALLOW_ENABLED'}) ? 'on' : 'off';
	$customlists{'block'}{'enabled'} = (defined $cgiparams{'BLOCK_ENABLED'}) ? 'on' : 'off';

	&_customlists_save_conf();
	&_customlist_export('allow', $RPZ_ALLOWLIST);
	&_customlist_export('block', $RPZ_BLOCKLIST);

	# Make new lists, request service reload on success
	$result = &General::system('/usr/sbin/rpz-make', 'allowblock', '--no-reload');
	return unless &_rpz_check_result($result, 1);

	return 1;
}

# Trigger rpz-config reload
sub _action_rpz_reload {
	return 1 unless &_rpz_needs_reload();

	# Immediately clear flag to prevent multiple reloads
	if(-f $RPZ_RELOAD_FLAG) {
		unlink($RPZ_RELOAD_FLAG) or die "Can't remove $RPZ_RELOAD_FLAG: $!";
	}

	# Perform reload, recreate reload flag on error to enable retry
	my $result = &General::system('/usr/sbin/rpz-config', 'reload');
	if(not &_rpz_check_result($result, 0)) {
		&General::safe_system('touch', "$RPZ_RELOAD_FLAG");
		return;
	}

	return 1;
}


###--- Internal rpz-config functions ---###

# Translate rpz-config exitcodes and messages
# 100-199: rpz-config, 200-299: webgui
sub _rpz_error_tr {
	my ($error, $append) = @_;
	$append //= '';

	# Translate numeric exit codes
	if(looks_like_number($error)) {
		if(defined $Lang::tr{"rpz exitcode $error"}) {
			$error = $Lang::tr{"rpz exitcode $error"};
		}
	}

	return "RPZ $Lang::tr{'error'}: $error" . &Header::escape($append);
}

# Check result of rpz-config system call, request reload on success
sub _rpz_check_result {
	my ($result, $request_reload) = @_;
	$request_reload //= 0;

	# exitcode 0 = success
	if($result != 0) {
		$errormessage = &_rpz_error_tr($result);
		return;
	}

	# Set reload flag
	if($request_reload) {
		&General::safe_system('touch', "$RPZ_RELOAD_FLAG");
	}

	return 1;
}

# Test whether reload flag is set
sub _rpz_needs_reload {
	return (-f $RPZ_RELOAD_FLAG);
}

# Validate a zonefile entry, returns rpz-config exitcode on failure. Use _rpz_check_result to verify.
# unique = check for unique name
sub _rpz_validate_zonefile {
	my ($name, $url, $remark, $unique) = @_;
	$unique //= 1;

	unless($name =~ /^[a-zA-Z0-9_]{1,32}$/) {
		return 101;
	}
	unless($url =~ /^[\w+\.:;\/\\&@#%?=\-~|!]{1,128}$/) {
		return 105;
	}
	unless($remark =~ /^[\w \-()\.:;*\/\\?!&=]{0,32}$/) {
		return 201;
	}

	# Check against already existing names
	if($unique) {
		foreach my $existing (keys %zonefiles) {
			if(lc($name) eq lc($existing)) {
				return 104;
			}
		}
	}

	return 0;
}

# Validate a custom list, returns number of rejected line on failure. Check for non-zero results.
# listref = array reference, cleanup = remove invalid entries instead of returning an error
sub _rpz_validate_customlist {
	my ($listref, $cleanup) = @_;
	$cleanup //= 0;

	foreach my $index (reverse 0..$#{$listref}) {
		my $row = @$listref[$index];
		next unless($row); # Skip/allow empty lines

		# Reject/remove everything besides wildcard domains and remarks
		if((not &General::validwildcarddomainname($row)) && (not $row =~ /^;[\w \-()\.:;*\/\\?!&=]*$/)) {
			unless($cleanup) {
				# +1 for user friendly line number and to ensure non-zero exitcode
				return $index + 1;
			}

			# Remove current row
			splice(@$listref, $index, 1);
		}
	}

	return 0;
}


###--- Internal misc functions ---###

# Send HTTP 303 redirect headers for post/request/get pattern
# (Must be sent before calling &Header::showhttpheaders())
sub _http_prg_redirect {
	my $location = "https://$ENV{'SERVER_NAME'}:$ENV{'SERVER_PORT'}$ENV{'SCRIPT_NAME'}";
	print "Status: 303 See Other\n";
	print "Location: $location\n";
}
