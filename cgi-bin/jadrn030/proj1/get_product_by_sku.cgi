#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
require "database.pl";

my $q = new CGI;
my $sku = $q->param("sku");
my $dbh = get_database_handle();
my $getProductBySku = $dbh->prepare_cached('SELECT sku, catID, venID, vendorModel, description, features, cost, retail, image from product where sku = ?');

die "Couldn't prepare queries" unless defined $getProductBySku;

$getProductBySku->execute($sku);

my $product = "";
while(my @row=$getProductBySku->fetchrow_array()) {
	foreach $item (@row) {
		$product .= "$item|";
	}
	$product = substr $product, 0, (length($product) - 1);
}
unless($product) {
	$product = 'invalid';
}

$getProductBySku->finish();
$dbh->disconnect();

print $q->header();
print $product;