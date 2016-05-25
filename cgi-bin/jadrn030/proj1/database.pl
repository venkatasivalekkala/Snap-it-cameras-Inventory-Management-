#!/usr/bin/perl

use DBI;

my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "jadrn030";
my $username = "jadrn030";
my $password = "sweet";
my $database_source = "dbi:mysql:$database:$host:$port";

sub get_database_handle {
	my $dbh = DBI->connect($database_source, $username, $password) or die 'Cannot connect to db';
	return $dbh;
}

1;