#!/usr/bin/perl
# Lekkala Venkatasiva Reddy
# Project1
use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use Crypt::SaltedHash;

my $q = new CGI;
my $cookie_sid_old = $q->cookie('jadrn013SID');
my $session_old = new CGI::Session(undef, $cookie_sid_old, {Directory=>'/tmp'});   
my $sid_old = $session_old->id;

#print $sid_old."mehul";
#print $cookie_sid_old;


##---------------------------- MAIN ---------------------------------------


if($sid_old eq $cookie_sid_old) {
    send_to_main();   
    } elsif(authenticate_user()) {
    create_session();
    send_to_main();
    
    }
else {
    send_to_login_error();
    }    
###########################################################################

###########################################################################
sub authenticate_user {
    #$q = new CGI;
    #print "auth";
    my $user = $q->param("user");
    my $password = $q->param("password");    
    open DATA, "</srv/www/cgi-bin/jadrn013/passwords.dat" 
        or die "Cannot open file.";
    @file_lines = <DATA>;
    close DATA;

    $OK = 0; #not authorized

    foreach $line (@file_lines) {
        chomp $line;
        ($stored_user, $stored_pass) = split /=/, $line;    
        if($stored_user eq $user && Crypt::SaltedHash->validate($stored_pass, $password)) {
            $OK = 1;
            last;
            }
        }
    return $OK;
    }
###########################################################################

###########################################################################
sub send_to_login_error {
    print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/perl/jadrn013/proj1/logout.cgi" />
</head><body></body>
</html>

END
    }  
    
###########################################################################
      
###########################################################################
sub create_session {

# args are DRIVER, CGI OBJECT, SESSION LOCATION
# default for undef is FILE, NEW SESSION, /TMP 
# for login.html, don't look for any existing session.
# Always start a new one.  Send a cookie to the browser.
# Default expiration is when the browser is closed.
# WATCH YOUR COOKIE NAMES! USE JADRNXXX_SID  
    my $session = new CGI::Session(undef, undef, {Directory=>'/tmp'});
    $session->expires('+1d');
    my $cookie = $q->cookie(jadrn013SID => $session->id);
    print $q->header( -cookie=>$cookie ); #send cookie with session ID to browser    
    my $sid = $session->id;
    $session->param("my_name", "siva");
}

sub send_to_main {
   
print <<END;
Content-type:  text/html \n\n

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
<h1> Snapit Cameras </h1>

<div id="menu">
<ul>
<li><a class="selected" href="/perl/jadrn013/proj1/newInventory.cgi">New Inventory</a></li>
<li><a href="/perl/jadrn013/proj1/editInventory.cgi">Edit Inventory</a></li>
<li><a href="/perl/jadrn013/proj1/deleteInventory.cgi">Delete Inventory</a></li>
<li><a href="/perl/jadrn013/proj1/logout.cgi">LogOut</a></li>
</ul>
</div>
  <div class="progressTextDiv"> Submitting Form...</div>
	<div class="successCenter" id ="confirmation"></div>

    <form  	  id="addProductForm"
              name="Validate"
              action="http://jadran.sdsu.edu/perl/jadrn013/proj1/confirm.cgi"
              method="post"
              enctype="multipart/form-data">
      

<!-- <div id= "content"> -->

<ul class="inlineobjects">
			<li><label class="title">SKU:<span class="astric">*</span></label></li>
            <li><input type="text" name="sku" id="sku" size="10" placeholder="ABC-123" maxlength="7"/></li>
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
            <li><textarea rows="4" cols="50" name="productfeatures" placeholder="Good, Best Clarity, etc." id="productfeatures" ></textarea></li>
</ul>
<ul class="inlineobjects">         
            <li><label class="title">Cost:<span class="astric">*</span></label></li> 
          \$\ <li><input type="text" name="cost" id="cost" placeholder="350.80" size="15" /></li>
</ul> 
<ul class="inlineobjects">         
            <li><label class="title">Retail:<span class="astric">*</span></label></li> 
          \$\ <li><input type="text" name="retail" id="retail" placeholder="500" size="15" /></li>
</ul> 
<ul class="inlineobjects"> 
         	<li><label class="title">Product Image:<span class="astric">*</span></label></li> 
            <li><input type="file" name="productimage" id="productimage" /></li>
            <input type="hidden" id="formType" name="formType" value="new">
</ul>

<div id="error_message"> 
</div>   

 <div id="button">  
        <input type="submit" value="Add" name="submit" class="formbutton" />
        <input type="reset" value="Clear" name="reset" class="formbutton" />
        </div> 

</form>

</body>
</html>

END
}
  
    










