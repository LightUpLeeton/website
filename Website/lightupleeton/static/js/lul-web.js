var map;
var userMarker = null;
var locations = new Array();
var markers = new Array();
var locating = false;
var geocoder_ = new google.maps.Geocoder();
var latLngBounds_ = null;

function initializeMap() {
    var mapOptions = {
        zoom: 8,
        center: new google.maps.LatLng(-34.5513933, 146.4066521),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
        
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
    
    //Initial location fetch
    fetchLocations();
    
    //Once map is ready wire up the other UI elements
    wireEvents();
    
}
//Hook up the map event
google.maps.event.addDomListener(window, 'load', initializeMap);

function fetchLocations() {
        $.ajax({
        type: 'GET',
        url: '/api/location',
        success: function(data, textStatus) {
            if(textStatus == "success") {
                
                //show the user marker, hardcoded to leeton to begin with
                var latLng_ = new google.maps.LatLng(-34.5513933, 146.4066521);
                
                //remove old user marker
                if(userMarker)
                    userMarker.setMap(null);
                    
                userMarker = new google.maps.Marker({
                    'map': map,
                    'position': latLng_,
                    'title': 'You are here'
                });
                map.setCenter(latLng_);

                //setup map bounds for userMarker
                latLngBounds_ = new google.maps.LatLngBounds();
                latLngBounds_.extend(userMarker.getPosition());
                
                locations = data.results;
                addMarkersToMap(true);
                
            }
            else {
                console.log("error")
            }
        }
    });
}

function wireEvents() {

    //Submit box
    $("#address-box").keydown(addressBoxKeyDown);
    $("#verify-button").click(verifyButtonClicked);
    $("#submit-button").click(submitButtonClicked);
    
    //Search box
    $("#centre-button").click(centreButtonClicked);
    $("#reset-button").click(fetchLocations);

    $("#print-button").click(function() {
        window.print();
    });

    $("#success-alert-close").click(function(event) {
        $("#submit-success-alert").hide();
    });
    $("#error-alert-close").click(function(event) {
        $("#submit-error-alert").hide();
    });
    
    //check boxes
    $("#check-current").change(function(event) {
        if(!$("#check-previous").attr('checked')) {
            $("#check-current").attr('checked', true);
        }
        else
            addMarkersToMap(false);
    });
    $("#check-previous").change(function() {
        if(!$("#check-current").attr('checked')) {
            $("#check-previous").attr('checked', true);
        }
        else
            addMarkersToMap(false);
    });

    /*
    google.maps.event.addListener(map, 'zoom_changed', function() {
        
        zoomLevel = map.getZoom();
    
        for(var index = 0; index < markers.length; index++) {

            var marker_ = markers[index];
            var icon_ = new google.maps.Icon();   
        }

    });
    */
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
            $("#address-box").val(response[0]['formatted_address']);
            
            var regex = new RegExp("^.*(Leeton NSW 2705, Australia|Yanco NSW 2703, Australia|Whitton NSW 2705, Australia)$");
            
            if($("#address-box").val().search(regex) == -1) {
                $('#address-box').removeClass("success-outline");
                $('#address-box').addClass("error-outline");
            }
            else {
                //Enable the submit button
                $('#address-box').removeClass("error-outline");
                $('#address-box').addClass("success-outline");
                $('#submit-button').attr("disabled", false);
            }
            
        }
        else {
            $('#address-box').removeClass("success-outline");
            $('#address-box').addClass("error-outline");
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
                            fetchLocations();
                            $('#address-box').removeClass("success-outline");
                            $('#address-box').removeClass("error-outline");
                        }
                        
                        
                    },
                    error: function(data, textStatus) {
                        $("#submit-error-alert").show();
                        $('#address-box').addClass("error-outline");
                    }
                });
                
        }
    });
    
}

/************************
Centre
************************/

function centreButtonClicked() {
    
    var addess_ = $('#centre-box').val();
    
    //geocode the address in the search bar
    geocoder_.geocode({'address': addess_}, function(response, statusCode){
        if (statusCode == google.maps.GeocoderStatus.OK) {
            $('#centre-box').val(response[0]['formatted_address']);
            
            var latLng_ = new google.maps.LatLng(response[0]['geometry']['location'].lat(), response[0]['geometry']['location'].lng());
        
            //remove old user marker
            if(userMarker)
                userMarker.setMap(null);
                
            userMarker = new google.maps.Marker({
                'map': map,
                'position': latLng_,
                'title': 'You are here'
            });
            map.setCenter(latLng_);
            map.setZoom(18);
            
            //setup map bounds for new userMarker
            //latLngBounds_ = new google.maps.LatLngBounds();
            //latLngBounds_.extend(userMarker.getPosition());
        }
    });
    
    
}

function addMarkersToMap(opt_initial) {
     
    opt_initial = typeof(opt_initial) != 'undefined' ? opt_initial : false;
    
     var current_ = $("#check-current").attr('checked');
     var previous_ = $("#check-previous").attr('checked');
     
     //remove old locations
    for(var index = 0; index < markers.length; index++) {
        markers[index].setMap(null);
    }
    
    //add the matching locations
    for(var index = 0; index < locations.length; index++) {
        
        if((current_ && locations[index]["current"]) || (previous_ && !locations[index]["current"])) {
        
            var latLng_ = new google.maps.LatLng(locations[index]["latitude"], locations[index]["longitude"]);
            
            var image_ = (locations[index]["current"] ? "/img/ornament_green_small.png" : "/img/ornament_red_small.png");
            
            var marker_ = new google.maps.Marker({
                'map': map,
                'position': latLng_,
                'icon': image_,
                'animation': google.maps.Animation.DROP,
                'title': locations[index]["address"]
            });
            markers.push(marker_);
            
            if(opt_initial)
                latLngBounds_.extend(latLng_);
        }
        
    }
    
    if(opt_initial && latLngBounds_)
        map.fitBounds(latLngBounds_);
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