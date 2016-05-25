#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
require "database.pl";

my $q = new CGI;

my $appHtml = "";

get_app_data();
get_category_options();
get_vendor_options();

print $q->header();
print $appHtml;

###########################################################################

###########################################################################
sub get_app_data() {
	open DATA, "</home/jadrn030/public_html/proj1/inventory.html" or die "Cannot open file.";
	@file_lines = <DATA>;
	close DATA;

	foreach $line (@file_lines) {
		$appHtml .= $line;
	}
}
###########################################################################

###########################################################################
sub get_category_options {
	my $placeholder = "#category_options#";
	my $dbh = get_database_handle();
	my $sth = $dbh->prepare("SELECT id, name FROM category ORDER BY name");
	$sth->execute();
	
	$replacement = "";
	while(my @row=$sth->fetchrow_array()) {
		$replacement .= "<option value=\"" . $row[0] . "\">" . $row[1] . "</option>\n";
	}
	
	$sth->finish();
	$dbh->disconnect();
	
	$appHtml =~ s/$placeholder/$replacement/g;
}
###########################################################################

###########################################################################
sub get_vendor_options {
	my $placeholder = "#vendor_options#";
	my $dbh = get_database_handle();
	my $sth = $dbh->prepare("SELECT id, name FROM vendor ORDER BY name");
	$sth->execute();
	
	$replacement = "";
	while(my @row=$sth->fetchrow_array()) {
		$replacement .= "<option value=\"" . $row[0] . "\">" . $row[1] . "</option>\n";
	}
	
	$sth->finish();
	$dbh->disconnect();
	
	$appHtml =~ s/$placeholder/$replacement/g;
}