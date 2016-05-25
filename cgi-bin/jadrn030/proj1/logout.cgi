#!/usr/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);

my $q = new CGI;
my $sid = $q->cookie('jadrn030SID') || undef;
my $session = new CGI::Session(undef, $sid, {Directory => '/tmp'});
$session->clear('username');
$session->delete();

my $cookie = $q->cookie(
    -name       => 'jadrn030SID',
    -value      => '',
    -expires    => '+1h');

open DATA, "</home/jadrn030/public_html/proj1/index.html" or die "Cannot open file.";
@file_lines = <DATA>;
close DATA;

my $printFile = 0;
my $loginHtml = "";

for($i = 0; $i <= $#file_lines; $i++) {
	if(chomp($file_lines[$i]) eq '<body>') {
		$printFile = 1;
	}
	elsif(chomp($file_lines[$i]) eq '</body>') {
		last;
	}
	else {
		$loginHtml .= $file_lines[$i];
	}
}

print $q->header( -cookie=>$cookie );
print $loginHtml;