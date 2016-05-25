#!/usr/bin/perl

use CGI;
use CGI::Carp qw (fatalsToBrowser);
use File::Basename;
require "database.pl";
require "upload_helper.pl";

my $q = new CGI;
my $newFilename = "";

upload_photo();
save_product_info();

print $q->header();
print 'success';

sub save_product_info {
	
	my $sku = $q->param("sku");
	my $category = $q->param("category");
	my $vendor = $q->param("vendor");
	my $model = $q->param("model");
	my $description = $q->param("description");
	my $features = $q->param("features");
	my $cost = $q->param("cost");
	my $retail = $q->param("retail");
	my $productImage = $q->param("productImage");
	
	my $dbh = get_database_handle();
	
	my $insertProductInfo;
	if(defined($productImage) && length $productImage) {
		$insertProductInfo = $dbh->prepare_cached('UPDATE product SET catID = ?, venID = ?, vendorModel = ?, description = ?, features = ?, cost = ?, retail = ?, image = ? WHERE sku = ?');
		
		die "Couldn't prepare queries" unless defined $insertProductInfo;
		
		$insertProductInfo->execute($category, $vendor, $model, $description, $features, $cost, $retail, $newFilename, $sku) or die "Failed to insert product data";
	}
	else {
		$insertProductInfo = $dbh->prepare_cached('UPDATE product SET catID = ?, venID = ?, vendorModel = ?, description = ?, features = ?, cost = ?, retail = ? WHERE sku = ?');
		
		die "Couldn't prepare queries" unless defined $insertProductInfo;
		
		$insertProductInfo->execute($category, $vendor, $model, $description, $features, $cost, $retail, $sku) or die "Failed to insert product data";
	}
	
	$insertProductInfo->finish();
	$dbh->disconnect();
	
}

sub upload_photo {
	
	my $sku = $q->param("sku");
	my $filename = $q->param("productImage");
	
	if(defined($filename) && length $filename) {
		
		my $upload_dir = get_upload_dir();
		my $safe_filename_chars = get_safe_filename_chars();
		
		unless($filename) {
			die "There was a problem uploading the image.";
		}
		
		my $mimetype = $q->uploadInfo($filename)->{'Content-Type'};
		if($mimetype !~ /image/) {
			die "Invalid mime type, $mimetype";
		}

		my ($name, $path, $extension) = fileparse($filename, qr"\..[^.]*$");
		$newFilename = $sku.$extension;
		$newFilename =~ s/ //;
		if($newFilename !~ /^([$safe_filename_chars]+)$/) {
			die "Sorry, invalid character in the filename.";
		}
		$newFilename = untaint($newFilename);
		$newFilename = lc($newFilename);

		my $filehandle = $q->upload("productImage");
		unless($filehandle) {
			die "Invalid handle";
		}

		open UPLOADFILE, ">$upload_dir/$newFilename" or die "Error, cannot save the file.";
		binmode UPLOADFILE;
		while(<$filehandle>) {
			print UPLOADFILE $_;
		}
		close UPLOADFILE;
		
	}
	
}