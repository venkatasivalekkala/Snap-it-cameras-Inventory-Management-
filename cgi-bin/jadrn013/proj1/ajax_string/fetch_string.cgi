#!/usr/bin/perl

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
print $sku;

my $query = "select sku, catID, venID, vendorModel, description, features, cost, retail,
  image from product where sku='$sku';";
            
my $sth = $dbh->prepare($query);
$sth->execute();

while(my @row=$sth->fetchrow_array()) {
    foreach $item (@row) {    
        $response .= $item."|"; #field separator
        }
    $response = substr $response, 0, (length($response)-1);  
    $response .= "||";  #record separator
    } 
    $response = substr $response, 0, (length($response)-2);     
unless($response) {
    $response = "invalid";
    }    
$sth->finish();
$dbh->disconnect();
    
print "Content-type: text/html\n\n";
print $response;               
