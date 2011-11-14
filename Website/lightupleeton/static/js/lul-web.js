var map;
var userMarker = null;
var markers = new Array();
var locating = false;
var geocoder_ = new google.maps.Geocoder();

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
        
    $("#success-alert-close").click(function(event) {
        $("#submit-success-alert").hide();
    });
}

/************************
Google Maps
*************************/

/************************
Verify
************************/

function addressBoxKeyDown() {
    $('#address-box').addClass("error");
    $('#submit-button').attr("disabled", true);
}

function verifyButtonClicked() {
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
                    success: function(data, textStatus) {
                        if(textStatus == "success") {
                            $("#submit-success-alert").show();
                            $("#address-box").val("");
                            $('#submit-button').attr("disabled", true);
                        }
                        else {
                            $("#submit-error-alert").show();
                        }
                    }
                });
                
        }
    });
    
}

/************************
Search
************************/

function searchButtonClicked() {
    
    var addess_ = $('#search-box').val();
    
    //geocode the address in the search bar
    geocoder_.geocode({'address': addess_}, function(response, statusCode){
        if (statusCode == google.maps.GeocoderStatus.OK) {
            $('#search-box').val(response[0]['formatted_address']);
            search(response[0]['geometry']['location'].lat(), response[0]['geometry']['location'].lng());
        }
    });
    
    
}

function search(latitude, longitude) {
    $.ajax({
        type: 'GET',
        url: '/api/location/all',
        data: {
            "latitude" : latitude,
            "longitude" : longitude
        },
        success: function(data, textStatus) {
            if(textStatus == "success") {
                
                //show the user marker, center the map
                var latLng_ = new google.maps.LatLng(latitude, longitude);
                
                //remove old user marker
                if(userMarker)
                    userMarker.setMap(null);
                
                userMarker = new google.maps.Marker({
                    'map': map,
                    'position': latLng_,
                    'title': 'You are here'
                });
                map.setCenter(latLng_);
                
                //remove old locations
                for(var index = 0; index < markers.length; index++) {
                    markers[index].setMap(null);
                }
                
                //setup map bounds
                var latLngBounds_ = new google.maps.LatLngBounds();
                latLngBounds_.extend(userMarker.getPosition());
                
                //add the matching locations
                for(var index = 0; index < data.results.length; index++) {
                    
                    var latLng_ = new google.maps.LatLng(data.results[index]["latitude"], data.results[index]["longitude"]);
                    
                    var image_ = (data.results[index]["current"] ? "/img/ornament_green.png" : "/img/ornament_red.png");
                    
                    var marker_ = new google.maps.Marker({
                        'map': map,
                        'position': latLng_,
                        'icon': image_,
                        'animation': google.maps.Animation.DROP
                    });
                    markers.push(marker_);
        
                    latLngBounds_.extend(latLng_);
                    
                }
                
                map.fitBounds(latLngBounds_);
                
            }
            else {
                console.log("error")
            }
        }
    });
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