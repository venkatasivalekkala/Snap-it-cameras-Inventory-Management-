#!/usr/bin/perl

use CGI;

$CGI::POST_MAX = 1024 * 3000;
my $safe_filename_chars = 'a-zA-Z0-9_.-';
my $upload_dir = '/home/jadrn030/public_html/proj1/_product_pics_';

sub get_safe_filename_chars {
	return $safe_filename_chars;
}
sub get_upload_dir {
	return $upload_dir;
}
sub untaint {
    if($_[0] =~ m/^(\w+)$/) { die "Tainted filename!"; }
    return $1;
}

1;