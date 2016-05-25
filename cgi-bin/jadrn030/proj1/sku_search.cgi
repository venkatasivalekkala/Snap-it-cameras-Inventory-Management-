#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
require "database.pl";

my $q = new CGI;
my $sku = $q->param("sku");
my $dbh = get_database_handle();
my $getSkuCount = $dbh->prepare_cached('SELECT count(*) from product where sku = ?');

die "Couldn't prepare queries" unless defined $getSkuCount;

$getSkuCount->execute($sku);

my $rowCount = -1;
if(my @row=$getSkuCount->fetchrow_array()) {
	$rowCount = $row[0];
}

print $q->header();
print $rowCount;