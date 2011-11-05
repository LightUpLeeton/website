var map;

function initializeMap() {
    var mapOptions = {
        zoom: 8,
        center: new google.maps.LatLng(-34.55139, 146.40665),
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };
        
    map = new google.maps.Map(document.getElementById('map'), mapOptions);
}

//Hook up the map event
google.maps.event.addDomListener(window, 'load', initializeMap);