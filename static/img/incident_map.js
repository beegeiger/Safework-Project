// Basic SafeWork Map //

"use strict";

let sf_cent = {lat: 37.772121, lng: -122.420850};


//////////////////////////////////////////////

function initMap() {
    let map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.772121, lng: -122.420850},
        zoom: 13
    });

    let infoWindow = new google.maps.InfoWindow({
        width: 150
    });

    $.get('/incidents.json', function(incidents)) {
    let incident, marker, html;

    for (let key in incidents) {
        incident = incidents[key];
        let icon = {
        url: 'https://openclipart.org/image/2400px/svg_to_png/206317/Map-Warning-Icon.png',
        scaledSize: new google.maps.Size(25, 38),
    }
            marker = new google.maps.Marker({
                position: new google.maps.LatLng(incident.latitude, incident.longitude),
                map: map,
                title: 'Incident Type:' + incident.description,
                icon: icon
            });
        
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

}}






















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