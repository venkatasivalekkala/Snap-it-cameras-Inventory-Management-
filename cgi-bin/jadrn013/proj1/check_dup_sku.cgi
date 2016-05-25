#!/usr/bin/perl
# Lekkala Venkatasiva Reddy
# Project1

use DBI;
use CGI;

my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "jadrn013";
my $username = "jadrn013";
my $password = "simple";
my $database_source = "dbi:mysql:$database:$host:$port";
my $response = "";

my $dbh = DBI->connect($database_source, $username, $password)
or die 'Cannot connect to db';

my $q = new CGI;
my $sku = $q->param("sku");

my $query = "select sku from product where sku='$sku';";

            
my $sth = $dbh->prepare($query);
$sth->execute();

$count = $sth->rows;

while(my @row=$sth->fetchrow_array()) {    
    $response = $row[0];
    }
if($response) {
    $response = "duplicate"; 
    }    
else {
    $response = "ok";
    }    
$sth->finish();
$dbh->disconnect();
    
print "Content-type: text/html\n\n";
print $response;               
