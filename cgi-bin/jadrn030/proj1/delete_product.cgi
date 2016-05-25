#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
require "database.pl";

my $q = new CGI;

delete_product();

print $q->header();
print 'success';

sub delete_product {
	
	my $sku = $q->param("sku");
	
	my $dbh = get_database_handle();
	
	my $deleteProduct = $dbh->prepare_cached('DELETE FROM product WHERE sku = ?');
	die "Couldn't prepare queries" unless defined $deleteProduct;
	
	$deleteProduct->execute($sku) or die "Failed to delete product data";
	
	$deleteProduct->finish();
	$dbh->disconnect();
	
}