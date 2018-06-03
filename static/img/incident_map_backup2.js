// Basic SafeWork Map //

"use strict";

let sf_cent = {lat: 37.772121, lng: -122.420850};

// this.scriptCache = cache({
//   google: 'https://api.google.com/some/script.js'
// });

// GoogleApi({
//   apiKey: "AIzaSyDqSXr_5uDcPRB4GEFIUUeIfP-GdZOz3Hg",
//   libraries: ['places']
// });


// const Container = React.createClass({
//   render: function() {
//     return "<div>Google</div>";
//     }
//   })

// export default GoogleApiComponent({
//   apiKey: "AIzaSyDqSXr_5uDcPRB4GEFIUUeIfP-GdZOz3Hg"
// })(Container)



//////////////////////////////////////////////
function initMap() {
    let styledMapType = new google.maps.StyledMapType(
                [
        {
          "featureType": "administrative",
          "elementType": "labels.text",
          "stylers": [
            {
              "color": "#00f5f1"
            },
            {
              "weight": 1.5
            }
          ]
        },
        {
          "featureType": "administrative",
          "elementType": "labels.text.stroke",
          "stylers": [
            {
              "color": "#0015ff"
            }
          ]
        },
        {
          "featureType": "administrative.land_parcel",
          "elementType": "geometry.stroke",
          "stylers": [
            {
              "color": "#6e0837"
            }
          ]
        },
        {
          "featureType": "administrative.locality",
          "elementType": "labels.text",
          "stylers": [
            {
              "saturation": 100
            },
            {
              "lightness": 95
            },
            {
              "weight": 8
            }
          ]
        },
        {
          "featureType": "administrative.locality",
          "elementType": "labels.text.fill",
          "stylers": [
            {
              "color": "#0a00ff"
            },
            {
              "weight": 4.5
            }
          ]
        },
        {
          "featureType": "administrative.locality",
          "elementType": "labels.text.stroke",
          "stylers": [
            {
              "color": "#1cfffc"
            },
            {
              "weight": 3.5
            }
          ]
        },
        {
          "featureType": "administrative.neighborhood",
          "elementType": "labels.text",
          "stylers": [
            {
              "lightness": -15
            }
          ]
        },
        {
          "featureType": "administrative.neighborhood",
          "elementType": "labels.text.stroke",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "landscape",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#3600ad"
            }
          ]
        },
        {
          "featureType": "landscape.natural",
          "elementType": "labels",
          "stylers": [
            {
              "color": "#000dff"
            }
          ]
        },
        {
          "featureType": "landscape.natural",
          "elementType": "labels.text.stroke",
          "stylers": [
            {
              "color": "#f975fc"
            }
          ]
        },
        {
          "featureType": "poi",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#000000"
            }
          ]
        },
        {
          "featureType": "poi",
          "elementType": "labels",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "poi.government",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#ff0000"
            }
          ]
        },
        {
          "featureType": "poi.park",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#000000"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#95298d"
            },
            {
              "lightness": -25
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "geometry.stroke",
          "stylers": [
            {
              "color": "#6e0837"
            },
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "labels.text",
          "stylers": [
            {
              "lightness": -25
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "labels.text.fill",
          "stylers": [
            {
              "color": "#6ad7f2"
            }
          ]
        },
        {
          "featureType": "road",
          "elementType": "labels.text.stroke",
          "stylers": [
            {
              "visibility": "off"
            }
          ]
        },
        {
          "featureType": "road.highway",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#f55ef9"
            }
          ]
        },
        {
          "featureType": "transit",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#6e0837"
            }
          ]
        },
        {
          "featureType": "water",
          "elementType": "geometry.fill",
          "stylers": [
            {
              "color": "#009fff"
            }
          ]
        }
      ],
        {name: 'Styled Map'});
    const map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.772121, lng: -122.420850},
        zoom: 13
    });
    map.mapTypes.set('styled_map', styledMapType);
    map.setMapTypeId('styled_map');

    var infoWindow = new google.maps.InfoWindow({});
    getPoints(map, infoWindow);
// Create the search box and link it to the UI element.
    // var input = document.getElementById('pac-input');
    // var searchBox = new google.maps.places.SearchBox(input);
    // map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    // map.addListener('bounds_changed', function() {
    //   searchBox.setBounds(map.getBounds());
    // });

    // var markers = [];
    // // Listen for the event fired when the user selects a prediction and retrieve
    // // more details for that place.
    // searchBox.addListener('places_changed', function() {
    //   var places = searchBox.getPlaces();

    //   if (places.length == 0) {
    //     return;
    //   }

    //   // Clear out the old markers.
    //   markers.forEach(function(marker) {
    //     marker.setMap(null);
    //   });
    //   markers = [];

    //   // For each place, get the icon, name and location.
    //   var bounds = new google.maps.LatLngBounds();
    //   places.forEach(function(place) {
    //     if (!place.geometry) {
    //       console.log("Returned place contains no geometry");
    //       return;
    //     }
    //     var icon = {
    //       url: place.icon,
    //       size: new google.maps.Size(71, 71),
    //       origin: new google.maps.Point(0, 0),
    //       anchor: new google.maps.Point(17, 34),
    //       scaledSize: new google.maps.Size(25, 25)
    //     };

    //     // Create a marker for each place.
    //     markers.push(new google.maps.Marker({
    //       map: map,
    //       icon: icon,
    //       title: place.name + incident.year,
    //       position: place.geometry.location,
    //       visible: true
    //     }));

    //     if (place.geometry.viewport) {
    //       // Only geocodes have viewport.
    //       bounds.union(place.geometry.viewport);
    //     } else {
    //       bounds.extend(place.geometry.location);
    //     }
    //   });
    //   map.fitBounds(bounds);
    // });
}

let image = '/static/img/Marker1.gif'
let num1 = 40
let num2 = 50
let opacity = 1.0

$(document).ready(function(){
  $( "#since2000" ).click(function(){
      deleteMarkers();
      initLoadGroupMarkers(this.value);
      console.log("2000 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2010" ).click(function(){
      initLoadGroupMarkers(this.value);
      console.log("2010 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2017" ).click(function(){
      initLoadGroupMarkers(this.value);
      console.log("2017 Button is working");
  });
});




function getPoints(map, infowindow) {
    $.get('/incidents.json', function(incidents) {
        // debugger;
    let incident, marker, html;
        var markers = [];
    for (let key in incidents) {
        incident = incidents[key];
        incident.year = parseInt(incident.year);
        if (incident.year > 2017) {
            image = '/static/img/Marker1.gif';
            num1 = 45;
            num2 = 60;
            opacity = 1.0;
        } else if (incident.year > 2016) {
            image = '/static/img/Marker2.gif';
            num1 = 43;
            num2 = 57;
            opacity = 0.95;
        } else if (incident.year > 2015) {
            image = '/static/img/Marker3.gif';
            num1 = 40;
            num2 = 53;
            opacity = 0.9;
        } else if (incident.year > 2014) {
            image = '/static/img/Marker4.gif';
            num1 = 37;
            num2 = 50;
            opacity = 0.85;
        } else if (incident.year > 2012) {
            image = '/static/img/Marker5.gif';
            num1 = 33;
            num2 = 45;
            opacity = 0.8;
        } else if (incident.year > 2010) {
            image = '/static/img/Marker6.gif';
            num1 = 30;
            num2 = 40;
            opacity = 0.7;
        } else if (incident.year > 2008) {
            image = '/static/img/Marker7.gif';
            num1 = 26;
            num2 = 35;
            opacity = 0.6;
        } else if (incident.year > 2005) {
            image = '/static/img/Marker8.gif';
            num1 = 22;
            num2 = 30;
            opacity = 0.5;
        } else if (incident.year > 2002) {
            image = '/static/img/Marker9.gif';
            num1 = 18;
            num2 = 25;
            opacity = 0.4;
        } else {
            image = '/static/img/Marker10.gif';
            num1 = 15;
            num2 = 20;
            opacity = 0.3;
        };
        let icon = {
        url: image,
        scaledSize: new google.maps.Size(num1, num2),
        opacity: opacity
    }   
        // console.log(incident.latitude, incident.longitude)
        incident.latitude = parseFloat(incident.latitude);
        incident.longitude = parseFloat(incident.longitude);
        marker = new google.maps.Marker({
            position : {lat: incident.latitude, lng: incident.longitude},
            map : map,
            title : 'Incident Type:' + incident.description,
            icon : icon,
        });
        markers.push(marker);
        window.incident = incident;
        html = (
          '<div class="' + incident.year + '" >' +
                '<p><b>'+ incident.description +'</b></p>' +
                '<p><b>'+ incident.incident_id +'</b></p>' +
                '<p><b>Address: </b>' + incident.address + '</p>' +
                '<p><b>City: </b>' + incident.city + '</p>' +
                '<p><b>State: </b>' + incident.state + '</p>' +
                '<p><b>Date: </b>' + incident.date + '</p>' +
                '<p><b>Time: </b>' + incident.time + '</p>' +
                '<p><b>Police Record Number: </b>' + incident.rec_number + '</p>' +
              '</div>');
        bindInfo(marker, map, html, infoWindow);
        };
    });
}




function bindInfo(marker, map, html, infoWindow) {
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