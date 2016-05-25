#!/usr/bin/perl
# Lekkala Venkatasiva Reddy
# Project1

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

my $q = new CGI;
my $cookie_sid = $q->cookie('jadrn013SID');
my $session = new CGI::Session(undef, $cookie_sid, {Directory=>'/tmp'});   
my $sid = $session->id;

if($cookie_sid ne $sid) {
    print <<END;
Content-type:  text/html\n\n

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/perl/jadrn013/proj1/logout.cgi" />
</head><body></body>
</html>

END
return;
}

print <<END;
Content-type: text/html \n\n


<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
    <meta http-equiv="Pragma" content="no-cache" />
    <meta http-equiv="Expires" content="0" />  
		
 <link rel="stylesheet" type="text/css" href="/~jadrn013/proj1/css/style.css" />   
<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script type="text/javascript" src="/~jadrn013/proj1/js/ajax_healper.js"></script>
<script type="text/javascript" src="/~jadrn013/proj1/js/validation.js"></script>
<script type="text/javascript">
		history.go(1)
	</script>
</head>

<body>
<h1>Snapit Cameras</h1>

      
<div id="menu">
<ul>
<li><a  href="/perl/jadrn013/proj1/newInventory.cgi">New Inventory</a></li>
<li><a  class="selected" href="/perl/jadrn013/proj1/editInventory.cgi">Edit Inventory</a></li>
<li><a href="/perl/jadrn013/proj1/deleteInventory.cgi">Delete Inventory</a></li>
<li><a href="/perl/jadrn013/proj1/logout.cgi">Logout</a></li>
</ul>
</div>

<div class="progressTextDiv"> Submitting Form...</div>
<div class="successCenter" id ="confirmation"></div>
<div id= "sku_form">
<form  	  id="fetchProductForm"
              method="post"
              enctype="multipart/form-data">
              
<div id="searchDiv">              
<input type="text" name="sku_search" id="sku_search" size="10" placeholder="ABC-123" maxlength="7" />
<input type="submit" value="Search" name="submit" class="formbutton" />
</div>

</form>
</div>
    <form  
              name="Validate"
              id="editProductForm"
              action="http://jadran.sdsu.edu/perl/jadrn013/proj1/confirm.cgi"
              method="post"
              enctype="multipart/form-data">


<!-- <div id= "content"> -->

<ul class="inlineobjects">
			<li><label class="title">SKU:</label></li>
            <li><input type="text" name="sku_readonly" id="sku" size="25" maxlength="7" readonly/></li>
</ul> 
<ul class="inlineobjects">            
             <li><label class="title">Category:<span class="astric">*</span></label></li>    
            <li><select name="category" id="category"></select> </li>
</ul> 
<ul class="inlineobjects"> 
			<li><label class="title">Vendor:<span class="astric">*</span></label></li> 
    		<li><select name="vender" id="vender"></select> </li>
</ul> 
<ul class="inlineobjects"> 
            <li><label class="title">Manufacturer's Identifier:<span class="astric">*</span></label></li> 
            <li><input type="text" name="manufacturersidentifier" id="manufacturersidentifier" size="25" /></li>
</ul> 
<ul class="inlineobjects">           
        	<li><label class="title">Description:<span class="astric">*</span></label></li> 
			<li><textarea rows="4" cols="50" name="description" id="description" ></textarea></li>
</ul> 
<ul class="inlineobjects">  
        	<li><label class="title">Product Features:<span class="astric">*</span></label></li> 
            <li><textarea rows="4" cols="50" name="productfeatures" id="productfeatures" ></textarea></li>
</ul>
<ul class="inlineobjects">         
            <li><label class="title">Cost:<span class="astric">*</span></label></li> 
          \$\ <li><input type="text" name="cost" id="cost" size="25" /></li>
</ul> 
<ul class="inlineobjects">         
            <li><label class="title">Retail:<span class="astric">*</span></label></li> 
          \$\ <li><input type="text" name="retail" id="retail" size="25" /></li>
</ul> 
<ul class="inlineobjects"> 
         	<li><label class="title">Product Image:<span class="astric">*</span></label></li> 
            <li><input type="file" name="productimage" id="productimage" /></li>
             <li><img id="prodImageView" src="" alt="product image" height="65" width="65"></li>
              <input type="hidden" name="formType" id="formType" value="edit">
</ul>

<div id="error_message"> 
</div>   

 <div id="button">  
        <input type="submit" value="Update" name="submit" class="formbutton" />
        <input type="reset" value="Clear" name="reset" class="formbutton" />
        </div> 

</form>
</body>
</html>
END
