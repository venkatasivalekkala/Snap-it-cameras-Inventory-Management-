#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Cookie;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

my $q = new CGI;
my $username = $q->param("username");
my $password = $q->param("password");   
open DATA, "</srv/www/cgi-bin/jadrn030/proj1/passwords.dat" or die "Cannot open file.";
@file_lines = <DATA>;
close DATA;

my $OK = 0;

foreach $line (@file_lines) {
	chomp $line;
	($stored_user, $stored_pass) = split /=/, $line;    
	if($stored_user eq $username && Crypt::SaltedHash->validate($stored_pass, $password)) {
		$OK = 1;
		last;
	}
}

if($OK) {
	my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
	$session->expires('+1d');
	$session->param('username',$username);
	my $cookie = $q->cookie(
		-name       => 'jadrn030SID',
		-value      => $session->id,
		-expires    => '+1h');
	print $q->header( -cookie=>$cookie );
	print "OK";
}
else {
	print $q->header();
	print "ERROR";
}