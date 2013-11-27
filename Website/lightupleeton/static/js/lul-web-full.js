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

function addMarkersToMap(opt_initial) {
     
    opt_initial = typeof(opt_initial) != 'undefined' ? opt_initial : false;
     
     //remove old locations
    for(var index = 0; index < markers.length; index++) {
        markers[index].setMap(null);
    }
    
    //add the matching locations
    for(var index = 0; index < locations.length; index++) {
        
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
    
    if(opt_initial && latLngBounds_)
        map.fitBounds(latLngBounds_);
}