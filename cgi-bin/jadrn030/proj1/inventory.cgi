#!user/bin/perl

use CGI;
use CGI::Session;
use CGI::Carp qw (fatalsToBrowser);
use DBI;

##---------------------------- MAIN ---------------------------------------

my $q = new CGI;
my $sid = $q->cookie('jadrn030SID') || undef;
my $session = new CGI::Session(undef, $sid, {Directory=>'/tmp'});

my $host = "opatija.sdsu.edu";
my $port = "3306";
my $database = "";
my $username = "jadrn030";
my $password = "sweet";
my $database_source = "dbi:mysql:$database:$host:$port";

if(defined $sid && $sid ne '') {
	send_to_inventory();
	}
else {
	send_to_login();
	}
###########################################################################

###########################################################################
sub send_to_login {
	$session->clear('username');
	$session->delete();
	
	my $cookie = $q->cookie(
		-name       => 'jadrn030SID',
		-value      => '',
		-expires    => '+1h');
	print $q->header( -cookie=>$cookie ); #send cookie with empty session ID to browser    
	print <<END;
Content-type:  text/html

<html>
<head>
    <meta http-equiv="refresh" 
        content="0; url=http://jadran.sdsu.edu/~jadrn030/proj1/" />
</head><body></body>
</html>

END
}

###########################################################################

###########################################################################
sub send_to_inventory {
	print <<END;
Content-type:  text/html


<!DOCTYPE html>

<!--    vander Duim, Jared    Account:  jadrn030
		CS645, Spring 2016
		Project #1
-->

<html>

	<head>
		<meta charset="utf-8">
		<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
		<meta http-equiv="Pragma" content="no-cache" />
		<meta http-equiv="Expires" content="0" />    
		<title>Inventory Management</title>
		
		<link rel="stylesheet" href="/~jadrn030/proj1/css/proj1.css">
		<link rel="stylesheet" href="/~jadrn030/proj1/css/inventory.css">
		<link rel="stylesheet" href="/~jadrn030/proj1/css/jquery-ui-1.11.4.custom/jquery-ui.theme.min.css">
		
		<script src="/jquery/jquery.js"></script>
		<script src="/jquery/jQueryUI.js"></script>
		<script src="/~jadrn030/proj1/js/inventory.js"></script>
	</head>

	<body>
		<div class="logoutDiv">
			<div class="logoutInnerDiv">
				<a href="/perl/jadrn030/proj1/logout.cgi">Logout</a>
			</div>
		</div>
		<div class="loginContainer">
			<div class="logoContainer">
				<img id="logo" src="/~jadrn030/proj1/images/logo.png" alt="cell-mate phones logo" />
				<div class="screenTitle">Inventory System</div>
			</div>
			<div>
				<div class="inventoryContentDiv">
					<div class="inventoryContentInnerDiv">
						<div id="accordion">
							<h3>New Item</h3>
							<div id="newRecordDiv">
								<form id="newForm" method="POST" action="/perl/jadrn030/proj1/new.cgi">
									<table>
										<tr>
											<td class="alignRight">
												<label for="sku">SKU</label>
											</td>
											<td>
												<input type="text" name="sku" id="sku" placeholder="SKU" size="7" maxlength="7">
											</td>
											<td class="alignRight">
												<label for="category">Category</label>
											</td>
											<td>
												<select>
													get_category_options()
												</select>
											</td>
											<td class="alignRight">
												<label for="vendor">Vendor</label>
											</td>
											<td>
												<input type="text" name="vendor" id="vendor" placeholder="Vendor" size="20" maxlength="20" />
											</td>
										</tr>
										<tr>
											<td class="alignRight">
												<label for="cost">Cost</label>
											</td>
											<td>
												<input type="number" name="cost" id="cost" size="6" min="0" value="0" />
											</td>
											<td class="alignRight">
												<label for="retail">Retail</label>
											</td>
											<td>
												<input type="number" name="retail" id="retail" size="6" min="0" value="0" />
											</td>
											<td class="alignRight">
												<label for="manufacturersId">Manufacturer's ID</label>
											</td>
											<td>
												<input type="text" name="manufacturersId" id="manufacturersId" placeholder="Manufacturer's ID" size="20" maxlength="20">
											</td>
										</tr>
										<tr>
											<td class="alignRight"><label for="description">Description</label></td>
											<td colspan="5">
												<textarea name="description" id="description"></textarea>
											</td>
										</tr>
										<tr>
											<td class="alignRight"><label for="features">Features</label></td>
											<td colspan="5">
												<textarea name="features" id="features"></textarea>
											</td>
										</tr>
									</table>
								</form>
							</div>
							<h3>Edit Item</h3>
							<div id="editRecordDiv">
								
								  Edit Record goes here.
							</div>
							<h3>Delete Item</h3>
							<div id="deleteRecordDiv">
								<p>
								  Delete Record goes here.
								</p>
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
	</body>
	
</html>

END
}
###########################################################################

###########################################################################
sub get_category_options {
	my $dbh = DBI->connect($database_source, $username, $password) or die 'Cannot connect to db';
	my $sth = $dbh->prepare("SELECT id, name FROM category ORDER BY name");
	$sth->execute();
	
	$str = "";
	while(my @row=$sth->fetchrow_array()) {
		$str .= '<option value="' . $row[0] . '">' . $row[1] . '</option>\n';
	}
	
	$sth->finish();
	$dbh->disconnect();
	
	print $str;
}