var map;
var locating = false;

function initializeMap() {
    var mapOptions = {
        zoom: 8,
        center: new google.maps.LatLng(-34.55139, 146.40665),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
        
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    
    //Once map is ready wire up the other UI elements
    wireEvents();
    
}
//Hook up the map event
google.maps.event.addDomListener(window, 'load', initializeMap);

function wireEvents() {

    //Submit box
    $("#address-box").keydown(addressBoxKeyDown);
    $("#verify-button").click(verifyButtonClicked);
    $("#submit-button").click(submitButtonClicked);
    
    //Search box
    $("#search-button").click(searchButtonClicked);
    
    //Locate button
    if(window.navigator.geolocation)
        $("#locate-button").click(locateButtonClicked);
    else
        $("#locate-button").hide();
}

/************************
Verify
************************/

function addressBoxKeyDown() {
    $('#address-box').addClass("error");
    $('#submit-button').attr("disabled", true);
}

function verifyButtonClicked() {
    var geocoder_ = new google.maps.Geocoder();
    geocoder_.geocode({'address': $("#address-box").val()}, function(response, statusCode){
        if (statusCode == google.maps.GeocoderStatus.OK) {
            //var location_ = response[0]['geometry']['location'];
            //this.facility_.setLattitude(location_.lat());
            //this.facility_.setLongitude(location_.lng());
            $("#address-box").val(response[0]['formatted_address']);
            
            //Enable the submit button
            $('#address-box').removeClass("error");
            $('#submit-button').attr("disabled", false);
            
        }
    });
}

/************************
Submit
************************/

function submitButtonClicked() {

    //grab the valid address
    var addess_ = $('#address-box').val();
    
    var geocoder_ = new google.maps.Geocoder();
    geocoder_.geocode({'address': addess_}, function(response, statusCode){
        if (statusCode == google.maps.GeocoderStatus.OK) {
                
                var location = {
                    "address" : response[0]['formatted_address'],
                    "latitude" : response[0]['geometry']['location'].lat(),
                    "longitude" : response[0]['geometry']['location'].lng()
                };
                
                $.ajax({
                    type: 'POST',
                    url: '/api/location',
                    data: JSON.stringify(location),
                    dataType: 'json',
                    success: function(data) {
                        console.log(data);
                    }
                });
                
        }
    });
    
}

/************************
Search
************************/

function searchButtonClicked() {
    console.log("click");   
}

/************************
Locate Me
************************/

function locateButtonClicked() {
    if(window.navigator.geolocation && !locating) {
        locating = true;
        navigator.geolocation.getCurrentPosition(locateSucceeded, locateFailed);
    }
}

function locateSucceeded(position) {
    locating = false;
    var geocoder_ = new google.maps.Geocoder();
    geocoder_.geocode({'latLng': new google.maps.LatLng(position.coords.latitude, position.coords.longitude)}, function(response, statusCode){
            if (statusCode == google.maps.GeocoderStatus.OK) {
                console.log(response[0]['formatted_address']);
                $("#search-box").val(response[0]['formatted_address']);
                //this.currentAddress_ = response[0]['formatted_address'];
            }
    });
    //this.search(position.coords.latitude, position.coords.longitude);
}

function locateFailed(error) {
    locating = false;
    
}