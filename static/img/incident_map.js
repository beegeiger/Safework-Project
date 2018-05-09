// Basic SafeWork Map //

"use strict";

let sf_cent = {lat: 37.772121, lng: -122.420850};


//////////////////////////////////////////////

function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.772121, lng: -122.420850},
        zoom: 13
    });
    getPoints(map);
}



function getPoints(map) {
    $.get('/incidents.json', function(incidents) {
    let incident, marker, html;
    
    console.log(incidents)
    for (let key in incidents) {
        incident = incidents[key];
        let icon = {
        url: 'https://openclipart.org/image/2400px/svg_to_png/206317/Map-Warning-Icon.png',
        scaledSize: new google.maps.Size(25, 38),
    }   
        // incident.latitude = incident.latitude
        // incident.longitude = incident.longitude
        marker = new google.maps.Marker({
            position: new google.maps.LatLng(incident.latitude, incident.longitude),
            // position: {lat: incident.latitiude,
            // lng: incident.longitude},
            map: map,
            title: 'Incident Type:' + incident.description,
            icon: icon
        });
        let infoWindow = new google.maps.InfoWindow({
        content: '<p>Marker Location:' + marker.getPosition() + '</p>'
    });
        console.log(marker)
        window.incident = incident;
        console.log(typeof incident.latitude)
        html = (
          '<div class="window-content">' +
                '<img src="https://openclipart.org/image/2400px/svg_to_png/206317/Map-Warning-Icon.png" alt="incident" style="width:150px;" class="thumbnail">' +
                '<p><b>Address: </b>' + incident.address + '</p>' +
                '<p><b>City: </b>' + incident.city + '</p>' +
                '<p><b>State: </b>' + incident.state + '</p>' +
                '<p><b>Date: </b>' + incident.date + '</p>' +
                '<p><b>Time: </b>' + incident.time + '</p>' +
                '<p><b>Police Record Number: </b>' + incident.rec_number + '</p>' +
              '</div>');
        bindInfoWindow(marker, map, infoWindow, html);
        }

    });
}
    

function bindInfoWindow(marker, map, infoWindow, html) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.close();
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
        });
}



// google.maps.event.addDomListener(window, 'load', initMap);

















        // function addMarker() {
    //     let icon = {
    //         url: 'https://openclipart.org/image/2400px/svg_to_png/206317/Map-Warning-Icon.png',
    //         scaledSize: new google.maps.Size(25, 38),
    //     }
    //     let marker = new google.maps.Marker({
    //         position: sf_cent,
    //         map: map,
    //         title: 'Hover text',
    //         icon: icon
    //     });
    //     return marker;