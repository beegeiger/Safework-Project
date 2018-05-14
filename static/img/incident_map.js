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

let image = '/static/img/Marker1.png'

function getPoints(map) {
    $.get('/incidents.json', function(incidents) {
    let incident, marker, html;
    for (let key in incidents) {
        incident = incidents[key];
        incident.year = parseInt(incident.year)
        if (incident.year === 2018) {
            image = '/static/img/Marker1.png'
        };
        if (incident.year === 2017) {
            image = '/static/img/Marker1.png'
        };
        if (incident.year === 2016) {
            image = '/static/img/Marker2.png'
        };
        if (incident.year === 2015) {
            image = '/static/img/Marker3.png'
        };
        if (incident.year === 2014) {
            image = '/static/img/Marker4.png'
        };
        if (incident.year === 2013) {
            image = '/static/img/Marker5.png'
        };
        if (incident.year === 2012) {
            image = '/static/img/Marker6.png'
        };
        if (incident.year === 2011) {
            image = '/static/img/Marker7.png'
        };
        if (incident.year === 2010) {
            image = '/static/img/Marker8.png'
        };
        if (incident.year === 2009) {
            image = '/static/img/Marker9.png'
        };
        if (incident.year === 2008) {
            image = '/static/img/Marker10.png'
        };
        if (incident.year === 2008) {
            image = '/static/img/Marker11.png'
        };
        let icon = {
        url: image,
        scaledSize: new google.maps.Size(50, 50),
    }   
        incident.latitude = parseFloat(incident.latitude);
        incident.longitude = parseFloat(incident.longitude);
        console.log(incident.address)
        if (incident.source_id == "4") {
            // console.log(incident);
            let inci = new google.maps.Geocoder();
            inci.geocode({'address': incident.address},
                function(results, status) {
                    if (status === google.maps.GeocoderStatus.OK) {
                        let marker = new google.maps.Marker({
                            map: map,
                            position: results[0].geometry.location
                        });
                    } else {
                        alert('Geocode was not successful for the following reason: ' + status);
                    }
            });
        }   
            else {
                marker = new google.maps.Marker({
                    // position: new google.maps.LatLng(incident.latitude, incident.longitude),
                    // position : {lat: incident.latitiude, lng: incident.longitude},
                    position : {lat: incident.latitude, lng: incident.longitude},
                    map : map,
                    title : 'Incident Type:' + incident.description,
                    icon : icon
                });
            }

        let infoWindow = new google.maps.InfoWindow({
        content : '<p>Marker Location:' + marker.getPosition() + '</p>'
            });
        

        
        window.incident = incident;

        html = (
          '<div class="window-content">' +
                '<p><b>'+ incident.description +'</b></p>' +
                '<p><b>Address: </b>' + incident.address + '</p>' +
                '<p><b>City: </b>' + incident.city + '</p>' +
                '<p><b>State: </b>' + incident.state + '</p>' +
                '<p><b>Date: </b>' + incident.date + '</p>' +
                '<p><b>Time: </b>' + incident.time + '</p>' +
                '<p><b>Police Record Number: </b>' + incident.rec_number + '</p>' +
              '</div>');
        // bindInfoWindow(marker, map, infoWindow, html);
        };
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