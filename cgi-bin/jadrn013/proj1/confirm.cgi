#!/usr/bin/perl
# LEKKALA VENKATASIVA REDDY
# Project1

use CGI;
use DBI;
use CGI::Carp qw (fatalsToBrowser);
use File::Basename;

####################################################################
### constants
$CGI::POST_MAX = 1024 * 3000; # Limit file size to 3MB
my $upload_dir = '/home/jadrn013/public_html/proj1/images/u_load_images';
my $safe_filename_chars = "a-zA-Z0-9_.-";
####################################################################

my $q = new CGI;

my $category;
my $sku;
my $vendor;
my $vendorid;
my $categoryId;
my $result = "";
my ($key, $value);
my $host = "opatija.sdsu.edu";
my $port = "3306";
my $formType="";

my $username = "jadrn013";
my $password = "simple";
my $isEditImagePresent = "false";

$database = "jadrn013";
$database_source = "dbi:mysql:$database:$host:$port";

my @key_arr = $q->param;

if(@key_arr < 2) 
{
	$result = "Please enter valid data.";
	print "Content-type: text/html\n\n";
    print $result;
   	exit;
} 
else 
{
for(my $i=0; $i<@key_arr; $i++) 
{
 my @value_ele = $q->param($key_arr[$i]);
 for(my $j=0; $j<@value_ele; $j++) 
 {
   if( $key_arr[$i] eq "category" ||
    $key_arr[$i] eq "vender" || $key_arr[$i] eq "manufacturersidentifier" ||
     $key_arr[$i] eq "description" || $key_arr[$i] eq "productfeatures" 
    || $key_arr[$i] eq "productimage")
  {

   if(isEmpty(trim($value_ele[$j]))) 
   {
   		$result = "$key_arr[$i] cannot be empty";
   		print "Content-type: text/html\n\n";
        print $result;
   		exit;
   }
  } elsif($key_arr[$i] eq "sku") {
  if(isSKU(uc $value_ele[$j]) == 0){
  	
  	$result = "invalid $key_arr[$i]";
  	print "Content-type: text/html\n\n";
	print $result;
  	exit;
   }
   }elsif( $key_arr[$i] eq "cost" || $key_arr[$i] eq "retail") {
   if(isValidAmount($value_ele[$j]) == 0) {
   $result = "invalid $key_arr[$i]";
   print "Content-type: text/html\n\n";
   print $result;
   exit;
   }
   }
 	}
  }
$formType = trim($q->param("formType"));
$sku =  uc trim($q->param("sku"));
$category =  trim($q->param("category"));
$vendor =  trim($q->param("vender"));


my $dbh = DBI->connect($database_source, $username, $password) 
or die 'Cannot connect to db';

if($formType eq "delete") {
my $imth = $dbh->prepare("SELECT image FROM product WHERE sku='$sku'");
$imth->execute()
or die 'Cannot insert values to db';

my @imageRow=$imth->fetchrow_array();
if(@imageRow != 0){
my $imageFile = "$upload_dir/$imageRow[0]";
if (unlink($imageFile) == 0) {
    print "File deleted successfully.";
} else {
    print "File was not deleted.";
}
}

my $wth = $dbh->prepare("DELETE FROM product WHERE sku='$sku'");
 $wth->execute()
or die 'Cannot insert values to db';
$wth->finish();
$dbh->disconnect();
# deleteCategoryIfAbsent($category, $dbh);
# deleteVendorIfAbsent($vendor, $dbh);
  
   print "Content-type: text/html\n\n";
   $result = "deleted";
   
   print $result;
   exit;

} else {

my $venderModel = trim($q->param("manufacturersidentifier"));
my $description = trim($q->param("description"));
my $features= trim($q->param("productfeatures"));
my $cost = trim($q->param("cost"));
my $retail = trim($q->param("retail"));
my $image = trim($q->param("productimage"));
my $filename = trim($q->param("productimage"));
my $epoch = time();
unless($filename) {
    die "There was a problem uploading the image; ";        
    }
      
my ($name, $path, $extension) = fileparse($filename, '/..*/');


$filename = $name.$extension;
$filename =~ s/ //; #remove any spaces
if($filename !~ /^([$safe_filename_chars]+)$/) {
    die "Sorry, invalid character in the filename.";
    }   

$filename = untaint($filename);
$filename = lc($filename);
my ($ext) = $filename =~ /(\.[^.]+)$/;
my $newName ="";
if($formType eq "edit" &&  $filename eq "undefined") {
$isEditImagePresent = "false";
} else {
if(isValidImage($ext) == 0) {
   $result = "Please upload valid image file";
   print "Content-type: text/html\n\n";
   print $result;
   exit;
}
# get a handle on the uploaded image     
my $filehandle = $q->upload("productimage"); 

unless($filehandle) { die "Invalid handle"; }

# save the file
open UPLOADFILE, ">$upload_dir/$filename" or die
    "Error, cannot save the file.";
binmode UPLOADFILE;
while(<$filehandle>) {
    print UPLOADFILE $_;
    }
close UPLOADFILE;
#print "$ext\n";
$newName = $sku.$ext;
rename("$upload_dir/$filename", "$upload_dir/$newName") || die ( "Error in renaming" );
$isEditImagePresent = "true";
}

print $formType;
if($formType eq "new") {
my $tth = $dbh->prepare("INSERT INTO product VALUES ('$sku', '$category', '$vendor', '$venderModel',
 '$description', '$features', '$cost', '$retail', '$newName')");
 $tth->execute()
or die 'Cannot insert values to db';
$tth->finish();
 $result="ok:";
   $result .= "<h3> Record inserted successfully!</h3>";
 } elsif($formType eq "edit") {
 my $queryString="";
 if($isEditImagePresent eq "true") {
 $queryString= "UPDATE product SET catID='$category', venID='$vendor', vendorModel='$venderModel',
 description='$description', features='$features', cost='$cost', retail='$retail', image='$newName' WHERE sku='$sku'";
 } else {
 $queryString= "UPDATE product SET catID='$category', venID='$vendor', vendorModel='$venderModel',
 description='$description', features='$features', cost='$cost', retail='$retail' WHERE sku='$sku'";
 }
 $uth = $dbh->prepare($queryString);
 $uth->execute()
or die 'Cannot insert values to db';
$uth->finish();
  $result="ok:";
   $result .= "<h3> Record Updated successfully!</h3>";
 }


$dbh->disconnect();
  
   # $result = "ok";
#    print "Content-type: text/html\n\n";
#    print $result;
#    exit;

#     if($formType eq "new" ||){
  
 
    $result .= "<table class='insertInventory'>";
    
my $query = "select sku, jadrn013.category.name, jadrn013.vendor.name, vendorModel, description, features, cost, retail,
  image from product, jadrn013.category, jadrn013.vendor where sku='$sku' AND jadrn013.category.categoryID='$category' AND jadrn013.vendor.vendorID='$vendor' ;";
            
my $fet = $dbh->prepare($query);
$fet->execute();

while(my @row=$fet->fetchrow_array()) {
$result .= "<tr><td>SKU</td><td>$row[0]</td></tr>";
$result .= "<tr><td>Category</td><td>$row[1]</td></tr>";
$result .= "<tr><td>Vendor</td><td>$row[2]</td></tr>";
$result .= "<tr><td>Manufacturer's Identifier</td><td>$row[3]</td></tr>";
$result .= "<tr><td>Description</td><td>$row[4]</td></tr>";
$result .= "<tr><td>Product Features</td><td>$row[5]</td></tr>";
$result .= "<tr><td>Cost</td><td>$row[6]</td></tr>";
$result .= "<tr><td>Retail</td><td>$row[7]</td></tr>";
$result .= "<tr><td>Product Image</td><td><img src = '/~jadrn013/proj1/images/u_load_images/$row[8]?$epoch' height='200px' width='200px' /></td></tr>";
$result .= "</table>";


  }
  
   
   print "Content-type: text/html\n\n";
   print $result;
   exit;
#    }
   
   
   
   }
}
  
sub isEmpty {
 foreach $item (@_){
      if($item eq "") {
      	return 1;
      } 
      	return 0;
   }
return 0;
}

sub isSKU
{
	my @parms = @_;
	$length = length($parms[0]);
	if($length == 7) {
	
    return $parms[0] =~/^[A-Z]{3}-[0-9]{3}$/; 
    } else {
    return 0;
    }
}

sub isValidAmount
{
	my @parms = @_;
    
    return $parms[0]=~ /^\d*[.]?\d+$/; 
}

sub isValidImage
{
	my @parms = @_;
	my $extension = $parms[0];
	
	if($extension eq ".gif" || $extension eq ".GIF" || $extension eq ".png" || $extension eq ".PNG" || $extension eq ".JPEG" || $extension eq ".jpeg" || $extension eq ".jpg" || $extension eq ".JPG")
     {
     #valid file
     return -1;
     
     } else 
     {
       return 0;
     } 

}

sub untaint {
    if($filename =~ m/^(\w+)$/) { die "Tainted filename!"; }
    return $1;
    }
    
sub trim {
    my @out = @_;
    for (@out) {
        s/^\s+//;
        s/\s+$//;
    }
    return $out[0];
}




