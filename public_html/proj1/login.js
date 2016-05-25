$(document).ready(function() {
    $("[name='user']").val('');
    $("[name='user']").focus();     

        
    $(':submit').on('click', function (e) {
        e.preventDefault();
        params = "user="+$("[name='user']").val()+"&password="+$("[name='password']").val();
        $.post('/perl/jadrn013/proj1/login.cgi', params, auth_handler);       
        });
        
    $('#main').on('click', '#logout',function() {       
        if(this.id == 'logout') {            
            $('#main').html('You are now logged out'); 
            $.get("/perl/jadrn013/proj1/logout.cgi", function() {})           
            }
        });
       
        
    });

function auth_handler(response) { 
    if (response === 'OK') {
        $.get("/perl/jadrn013/proj1/newInventory.cgi", app_handler);
        }               
    else 
       $('#status').text("ERROR, incorrect username or password ");
    }
    
function app_handler(response) {
    $('#main').html(response);
    }    
