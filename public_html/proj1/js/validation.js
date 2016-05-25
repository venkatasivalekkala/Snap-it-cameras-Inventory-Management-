
// LEKKALA VENKATASIVA REDDY
// Project1

var sku;
var category;
var vender;
var manufacturersIdentifier;
var description;
var productFeatures;
var cost;
var retail;
var productImage;
var infoArray;
var userName;
var password;
var isDuplicate;

var inputType = 
    {
    	IDENTICODE:0, TEXT:1,  NUMBER:2, DROPDOWN:3, AMOUNT:4, PHOTO:5
    };
     
//error message divs
var ErrorMessage = "error_message";

$(document).ready(function()
{ 
 	updateProgressText(false);
 	$formTypeForThisPage = $('#formType').val();
 	$inSKU = $('#sku').val();
 
 	fetchCategoryString();
 	fetchVendorString();
 	
 	if($formTypeForThisPage == "edit") {
 	$("input[type='reset']").on("click", function(event){
	 event.preventDefault();
 	 $('#category').val('');
    $('#vender').val('');
    $('#manufacturersidentifier').val('');
    $('#description').val('');
    $('#productfeatures').val('');
 	$('#cost').val('');
 	$('#retail').val('');
 	$('#productimage').val('');

 });
 	
 	} else if($formTypeForThisPage == "delete") {
 	$("input[type='reset']").on("click", function(event){
	 event.preventDefault();
 	resetFormInfo();
 	
 	$('#deleteProductForm').hide();
 	$('#sku_search').focus();
 	});
 	
 	}
 
 	if($formTypeForThisPage == "edit") 
 	{
 		$('#editProductForm').hide();
 	}
 	else if($formTypeForThisPage == "delete") 
 	{
 		$('#deleteProductForm').hide();
 	}
 
	function updateProgressText(isVisible)
  	{
  		if(isVisible) 
  		{
  			$('.progressTextDiv').show();
			$('#addProductForm').fadeTo(0, 0.3);
  			$('#fetchProductForm').fadeTo(0, 0.3);
  			$('#editProductForm').fadeTo(0, 0.3);
  			$('#menu').fadeTo(0, 0.3);
  			//document.getElementById("submitButton").disabled = true;
  			//document.getElementById("resetButton").disabled = true;
  		}
  		else
   		{
  			$('.progressTextDiv').hide();
  			$('#addProductForm').fadeTo(0, 1);
  			$('#fetchProductForm').fadeTo(0, 1);
  			$('#editProductForm').fadeTo(0, 1);
  			$('#menu').fadeTo(0, 1);
  			//document.getElementById("submitButton").disabled = false;
  			//document.getElementById("resetButton").disabled = false;
  		}
  	}
  
 	$("#sku_search").on( "keyup", function( event ) {
   		updateSKUBox("#sku_search", event);
 	});
 
 	$( "#sku" ).on( "keyup", function( event ) {
 		updateSKUBox("#sku", event);
  	});
 		
 	var url = window.location.href; 
    var isSubmitForm = false;
    var isError = false;
    var formData;
    var currentPage;

    $('#fetchProductForm').submit(function(e){
        fetchProductString();
        return false;         
  	});
 		
    $('#addProductForm').submit(function(e){
        submitFormData("new");
        return false;         
  	});
  
    $('#editProductForm').submit(function(e){
        submitFormData("edit");
        return false;         
  	});
  
  	$('#deleteProductForm').submit(function(e){
        submitFormData("delete");
        return false;         
  	});
  
	function handleSKU(response) 
  	{
    	if($.trim(response) == "ok") 
    	{
    		valid = true;
        	document.getElementById("sku").style.borderColor="#ffffff";
        	$('#error_message').html("");
        	isDuplicate = false;
			return;
		}
		isDuplicate = true;
    	document.getElementById("sku").style.borderColor="red";
    	$('#error_message').html("Duplicate SKU. Please enter unique SKU");
    }
  
	function updateSKUBox($skuInput, $eve) 
	{
  		$whichEvent = $eve.which;
 		
 		if($whichEvent != 8) 
 		{
			$skuin = $($skuInput).val().trim();
   			if($skuin.length == 3) 
   			{
   				$skuin = $skuin.toUpperCase();
   				$($skuInput).val($skuin+"-");
   			} 
   			else if($skuin.length == 7 && $formTypeForThisPage == "new") 
   			{
        		var url = 'http://jadran.sdsu.edu/perl/jadrn013/proj1/check_dup_sku.cgi';
        		url += '?sku=' + $('#sku').val();
        		$.get(url, handleSKU);
   			}
  		}
	}
  
   function submitFormData(formType)
   {
    	if(isSubmitForm == true) 
        {
            return true;
        }
        if(formType == "delete") 
        {
            handleAnswer("OK", formType);
            return isSubmitForm;
        }
        if(validateform(formType) != false) 
        {
            handleAnswer("OK", formType);
            return isSubmitForm;
        } 
        else 
        {
            return false;
        }
	}
  
	function fetchProductString()
  	{
  		var request = new HttpRequest(
        "http://jadran.sdsu.edu/perl/jadrn013/proj1/ajax_string/fetch_string.cgi?sku="+document.getElementById("sku_search").value, handle_string_data);   
    	request.send();
  	}
  
  	function fetchCategoryString()
  	{
  		var request = new HttpRequest(
        "http://jadran.sdsu.edu/perl/jadrn013/proj1/ajax_string/fetch_category.cgi", handle_cat_data);   
    	request.send();
  	}
  
  	function fetchVendorString()
  	{
  		var request = new HttpRequest(
        "http://jadran.sdsu.edu/perl/jadrn013/proj1/ajax_string/fetch_vendor.cgi", handle_vendor_data);   
    	request.send();
  	}
  	
  	function handle_cat_data(response) 
  	{
		if(response) 
		{
		
		console.log(response);
 	 	if(response == "invalid user") {
 	 	window.location = "http://jadran.sdsu.edu/~jadrn013/proj1/index.html";
        return;
 	 	
 	 	}
    		var items = response.split('||');
    		var categoryHandle = $('#category');
    		categoryHandle.append($('<option value="">Select Category</option>'))
    		for(i=0; i < items.length; i++) 
    		{
        		var pairs = items[i].split('=');     
        		categoryHandle.append($('<option></option>').
            	attr('value',pairs[0]).text(pairs[1]));
            }
  		}
	}
  
	function handle_vendor_data(response) 
	{
		if(response) 
		{
		
		console.log(response);
 	 	if(response == "invalid user") {
 	 	window.location = "http://jadran.sdsu.edu/~jadrn013/proj1/index.html";
        return;
 	 	
 	 	}
    		var items = response.split('||');
    		var vendorHandle = $('#vender');
    		vendorHandle.append($('<option value="">Select Vendor</option>'))
    		for(i=0; i < items.length; i++) 
    		{
        		var pairs = items[i].split('=');     
        		vendorHandle.append($('<option></option>').
            	attr('value',pairs[0]).text(pairs[1]));
            }
  		}
	}
  
	function handle_string_data(response)
  	{
	  	if(response) 
 	 	{
 	 	console.log(response);
 	 	if(response == "invalid user") {
 	 	window.location = "http://jadran.sdsu.edu/~jadrn013/proj1/index.html";
        return;
 	 	
 	 	}
			var fields = new Array();
   			fields = response.split("|");
   			if(fields.length > 0) 
   			{
   				if(fields[0] == "invalid") 
   				{
   					$('#error_message').html("No records found");
       		  		if($formTypeForThisPage == "edit") 
         			{
        				$('#editProductForm').hide();      
 					} 
 					else if($formTypeForThisPage == "delete") 
 					{
        				$('#deleteProductForm').hide();      
 					}
   				} 
   				else 
   				{
   					$('#error_message').html("");
   					$inSKU = fields[0];
   					var date = new Date();
	   				var epoch = date.getTime();
   					document.getElementById("sku").value = fields[0];
					document.getElementById("category").value = fields[1];
					document.getElementById("vender").value = fields[2];
					document.getElementById("manufacturersidentifier").value = fields[3];
					document.getElementById("description").value = fields[4];
					document.getElementById("productfeatures").value = fields[5];
					document.getElementById("cost").value = fields[6];
					document.getElementById("retail").value = fields[7];
					document.getElementById("prodImageView").src = "/~jadrn013/proj1/images/u_load_images/"+fields[8]+"?"+epoch;
	
  		      		if($formTypeForThisPage == "edit") 
        			{
        				$('#editProductForm').show();      
 					} 
 					else if($formTypeForThisPage == "delete") 
 					{
        				$('#deleteProductForm').show();      
 					}
 				}
			}	 
		}
	}
  
    function handleAnswer(answer, formType) 
    {
        if($.trim(answer) == "OK")  
        {
        	updateProgressText(true);
        	var form_data = new FormData($('form')[0]);  
        	if(formType == "delete") 
        	{
        		form_data.append("sku", document.getElementById("sku").value);
      			form_data.append("formType", formType);
        	} 
        	else 
        	{
          		form_data.append("sku", document.getElementById("sku").value); 
        		form_data.append("category", document.getElementById("category").value);
       			form_data.append("vender", document.getElementById("vender").value);
        		form_data.append("manufacturersidentifier", document.getElementById("manufacturersidentifier").value);
        		form_data.append("description", document.getElementById("description").value);
        		form_data.append("productfeatures", document.getElementById("productfeatures").value);
        		form_data.append("cost", document.getElementById("cost").value);
        		form_data.append("retail", document.getElementById("retail").value);
        		form_data.append("productimage", document.getElementById("productimage").files[0]);
        		form_data.append("formType", document.getElementById("formType").value);
    		}
        
			$.ajax({
            url: "/perl/jadrn013/proj1/confirm.cgi",
            type: "post",
            data: form_data,
            processData: false,
            contentType: false,
            
            success: function(response) 
            {
            console.log(response);
            	updateProgressText(false);
            	 if(response =='deleted') 
            	 {
             		resetFormInfo();
             		isError=false;
              		isSubmitForm = true;
              		$('#deleteProductForm').hide(); 
              		$("#sku_search").focus();
              		$("#confirmation").html(" Record with SKU "+$inSKU+" is deleted ");
					$('#confirmation').show();
              		isSubmitForm = false;
             	} 
             	else
             	{
              		var responseArray = response.split(':');
              		if(responseArray.length > 1) {
              		if(responseArray[0].trim() =='ok') 
              		{
              			isError=false;
              			isSubmitForm = true;

            			$('form').hide(10, function(){
            				document.getElementById('confirmation').innerHTML = responseArray[1];
            				$('#confirmation').show();
            				$('#menu').show();
            				$('h2').hide();
            				$('.newInventory').click(function(){
            					$('#confirmation').html('');
            					$('#menu').show();
            					$('#confirmation').hide();
            					resetFormInfo();
            					$('h2').show();
            					if($formTypeForThisPage == "new") 
            					{
            						$('form').show();
            						$("#sku").focus();
            						
            					} 
            					else 
            					{
            						$('#fetchProductForm').show();
            						$("#sku_search").focus();
            					}
            					isSubmitForm = false;
  							});
            			});
            		} else  if(responseArray[0].trim() =='error' && responseArray[1].trim() =='Invalid user') 
              		{
              		window.location = "http://jadran.sdsu.edu/~jadrn013/proj1/index.html";
              		}
            		}
            		else 
              		{
              		console.log("server error");
              			isError=true;
              			$('#error_message').html(response);
              			window.location = "http://jadran.sdsu.edu/~jadrn013/proj1/index.html";
              		} 
              	}
            },
            error: function(response) 
            {
            	updateProgressText(false);
            	$('#error_message').html(response);
            }
        });
            
    }
    else if ($.trim(answer) == "DUP")
        $('#status').html("ERROR, Duplicate");
    else
        $('#status').html("Database error");        
    }
        
    function handleAjaxPost(returnResult) 
    {
        if(returnResult !='ok') 
        {
            isError=true;
            $('#error_message').html(returnResult);
    	} 
        else 
        {
            isError=false;
            isSubmitForm = true;
        }       
    }   
 	$("#sku").focus(); 
 	$("#sku_search").focus(); 
	
	$('#EditInventory').on('click', function (e) {
        $.get('/perl/jadrn013/proj1/editInventory.cgi', auth_handler);       
        });
	
	
}); 

function app_handler(response) {
    $('#menu').html(response);
    } 
              
function resetFormInfo() 
{
    $('#sku_search').val('');
    $('#sku').val('');
    $('#category').val('');
    $('#vender').val('');
    $('#manufacturersidentifier').val('');
    $('#description').val('');
    $('#productfeatures').val('');
 	$('#cost').val('');
 	$('#retail').val('');
 	$('#productimage').val('');
 	
 	if(document.getElementById("prodImageView")) 
 	{
 		document.getElementById("prodImageView").src ="";
 	}
 }
    
function initVariables() 
{
	sku = {
        ID:"sku", TYPE:inputType.IDENTICODE, ERROR:"Please enter valid SKU.", ERROR_DIV_ID:"error_message", NAME:"sku"
     }
      
	category={
         ID:"category", TYPE:inputType.DROPDOWN, ERROR:"Please select category.", ERROR_DIV_ID:"error_message", NAME:"category"
    }
     
    vender={
         ID:"vender", TYPE:inputType.DROPDOWN, ERROR:"Please select vendor.", ERROR_DIV_ID:"error_message", NAME:"vendor"
    }  
     
    manufacturersIdentifier = {
          ID:"manufacturersidentifier", TYPE:inputType.TEXT, ERROR:"Please enter manufacturers identifier.", ERROR_DIV_ID:"error_message", NAME:"manufacturers identifier"
     }
     
     description = {
          ID:"description", TYPE:inputType.TEXT, ERROR:"Please enter valid description.", ERROR_DIV_ID:"error_message", NAME:"description"
     }
     
     productFeatures={ 
          ID:"productfeatures", TYPE:inputType.TEXT, ERROR:"Please enter valid product features.", ERROR_DIV_ID:"error_message", NAME:"product features"
     }
     
     cost={
         ID:"cost", TYPE:inputType.AMOUNT, ERROR:"Please enter valid cost price.", ERROR_DIV_ID:"error_message", NAME:"cost"
     }
     
    retail={
         ID:"retail", TYPE:inputType.AMOUNT, ERROR:"Please enter valid retail price.", ERROR_DIV_ID:"error_message", NAME:"retail"
     }
    
    productImage={
     ID:"productimage", TYPE:inputType.PHOTO, ERROR:"Please upload product image.", ERROR_DIV_ID:"error_message", NAME:"product image"
    }
     
    infoArray = [sku, category, vender, manufacturersIdentifier, description, productFeatures, cost, retail, productImage];
    
    for(var i=0; i<infoArray.length; i++) 
    {
     	var obj = infoArray[i];
     	document.getElementById(obj.ID).addEventListener("blur", getBlurFunction(obj), false);  
    }
 
    function getBlurFunction(obj) 
    {
        return function() 
        {
        validateOnBlur(obj);
        }
    }
}

function validateOnBlur(obj)
{
	if(isDuplicate)
	{
		return false;
	} 
	else 
	{
		if(checkEmptyValue(obj, false) == false) 
		{
			return false;
		}
		if(validateInput(obj, false) == false) 
		{
    		return false;
		}
    	clearError(obj);
    }
}

function validateInput(obj, isShowError) 
{
	switch(obj.TYPE) 
    { 
        case inputType.IDENTICODE:
                if(validateSKU(obj, isShowError) == false) 
                {
                    return false;
                }
                break;
        
        case inputType.DROPDOWN:
        		if(validateDropdownList(obj, isShowError)==false) 
        		{
           			return false;
        		}
        		break;
                                  
        case inputType.AMOUNT:
                if(validateAmount(obj, isShowError) == false) 
                {
                    return false;
                }
                break;

        case inputType.PHOTO:
                if(validatePhoto(obj, isShowError) == false) 
                {
                    return false;
                }
                break;
    }
}  

function checkEmptyValue(obj, isShowError) 
{
    var value = getValueFromId(obj.ID);
    if(isEmpty(value)) 
    {
        if(isShowError) 
        {
            showErrorDiv(obj, true);
        }
        return false;
    }
    return true;
}

function validateform(formType)
 {
    if(!infoArray) 
    {
    	initVariables();
    }
    if(isDuplicate)
    {
		return false;
	}
	else 
	{
     	clearAllErrorMessages();
     
     	//check input types and show error message if input is empty or invalid
    	for(var i= 0; i<infoArray.length; i++) 
    	{
    		if(infoArray[i].TYPE == inputType.PHOTO && formType == "edit" ) 
    		{
    			//dont check for empty in edit mode.
    		} 
    		else if(checkEmptyValue(infoArray[i], true) == false) 
    		{
       		 	return false;
       	 	}
    		if(validateInput(infoArray[i], true) == false) 
        	{
           		return false;
        	}
    	}    
 	}
 }
  
function validateDropdownList(obj, isShowError)
{
    if(isEmpty(document.getElementById(obj.ID).value.trim()) == false)
    {
         return true;  
    }  
    else  
    {  
        if(isShowError) 
        {
        	showErrorDiv(obj, true);
        }
        return false;  
    } 
}

function validatePhoto(obj, isShowError)
{
     var value = getValueFromId(obj.ID);
     
     if(isEmpty(value))
     {
		return true;
     }   
     var fileUpload = value;
     var extension = fileUpload.substring(fileUpload.lastIndexOf('.') + 1);
     
     //checking below extentions for photos
    if(extension == "gif" || extension == "GIF" || extension == "png" || extension == "PNG" || extension == "JPEG" || extension == "jpeg" || extension == "jpg" || extension == "JPG")
    {
        return true;
    } 
	else
    {
        if(isShowError) 
        {
        	document.getElementById(obj.ERROR_DIV_ID).innerHTML = "Please upload valid Image. Only JPEG/JPG/PNG/GIF file is allowed ";
        	document.getElementById(obj.ID).style.borderColor="red";
        	document.getElementById(obj.ID).focus();
        }
    	return false;
    }         
}
   
function validateusernamepassword(obj, isShowError)
{
	if(isEmpty(document.getElementById(obj.ID).value.trim()) == false)
    {
         return true;  
    }  
    else  
    {  
        if(isShowError) 
        {
       		showErrorDiv(obj, true);
        }
        return false;  
    } 
}

function validateAmount(obj, isShowError)
{
     var value = getValueFromId(obj.ID);
     
    if(isValidAmount(value))
    {
        return true;  
    }  
    else  
    {
        if(isShowError) 
        {
        	showErrorDiv(obj, false);
        }
        return false;  
    }  
}

function validateSKU(obj, isShowError)
{
	var value = getValueFromId(obj.ID);
	
     if(value.length == 7)
     {
    	if(isSKU(value))
    	{
        	return true;  
    	}  
    	else  
    	{
        	if(isShowError) 
        	{
        		showErrorDiv(obj, false);
        	}
        	return false;  
    	}
    }
    else
    {
    	if(isShowError) 
    	{
    		showErrorDiv(obj, false);
    	}
    	return false;  
	}  
}

     /*Helper Functions*/ 
function isEmpty(value)
{
    if(value !="")
    {
        return false;
    }
    else 
    {
       return true;
    }
}

function isValidAmount(value)
{
    var amountExpression = /^\d*[.]?\d+$/;
    return value.match(amountExpression); 
}  

function isNumber(value)
{
    var numberExpression = /^[0-9]+$/;
    return value.match(numberExpression); 
}  
 
     
function isText(value)
{
    var textExpression=/^[a-zA-Z]+$/;
    return value.match(textExpression);
}

function isSKU(value)
{
    var SKUExpression= /^[A-Z]{3}-[0-9]{3}$/;
    return value.match(SKUExpression);
}
    
    //clear all red borders and error messages.
function clearAllErrorMessages() 
{
    clearAllErrors();
    clearAllErrorBorder();
}
     
function clearAllErrorBorder() 
{
    for(var i=0; i<infoArray.length; i++) 
    {
    	clearError(infoArray[i]);
    }
}
     
function clearError(obj) 
{
	clearAllErrors();
	var id = obj.ID;
    if(id == "inlineDiv") 
    {
        document.getElementById(obj.ID).style.borderColor="#ffffff";
    } 
    else 
    {
        document.getElementById(obj.ID).style.borderColor="#dddddd";
    }
}

function clearAllErrors() 
{
	document.getElementById("error_message").innerHTML = "";
}
       
function getValueFromId(id) 
{
    return document.getElementById(id).value.trim();
}
     
function showErrorDiv(obj, isEmpty)
{
    if(isEmpty) 
    {
        if(obj.TYPE == inputType.PHOTO) 
        {
            document.getElementById(obj.ERROR_DIV_ID).innerHTML = obj.ERROR;
            
        } else if(obj.TYPE == inputType.DROPDOWN) {
        
        document.getElementById(obj.ERROR_DIV_ID).innerHTML = 'Please select ' + obj.NAME;
        }
        else 
        {
            document.getElementById(obj.ERROR_DIV_ID).innerHTML = 'Please enter ' + obj.NAME;
        }
    } 
    else 
    { 
        document.getElementById(obj.ERROR_DIV_ID).innerHTML = obj.ERROR; 
    }
    document.getElementById(obj.ID).style.borderColor="red";
    document.getElementById(obj.ID).focus();
}
    
    