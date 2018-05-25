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
    let map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.772121, lng: -122.420850},
        zoom: 13
    });
    map.mapTypes.set('styled_map', styledMapType);
    map.setMapTypeId('styled_map');
    let infoWindow = new google.maps.InfoWindow({});
    getPoints(map, infoWindow = infoWindow);
// Create the search box and link it to the UI element.
    var input = document.getElementById('pac-input');
    var searchBox = new google.maps.places.SearchBox(input);
    map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

    // Bias the SearchBox results towards current map's viewport.
    map.addListener('bounds_changed', function() {
      searchBox.setBounds(map.getBounds());
    });

    var markers = [];
    // Listen for the event fired when the user selects a prediction and retrieve
    // more details for that place.
    searchBox.addListener('places_changed', function() {
      var places = searchBox.getPlaces();

      if (places.length == 0) {
        return;
      }

      // Clear out the old markers.
      markers.forEach(function(marker) {
        marker.setMap(null);
      });
      markers = [];

      // For each place, get the icon, name and location.
      var bounds = new google.maps.LatLngBounds();
      places.forEach(function(place) {
        if (!place.geometry) {
          console.log("Returned place contains no geometry");
          return;
        }
        var icon = {
          url: place.icon,
          size: new google.maps.Size(71, 71),
          origin: new google.maps.Point(0, 0),
          anchor: new google.maps.Point(17, 34),
          scaledSize: new google.maps.Size(25, 25)
        };

        // Create a marker for each place.
        markers.push(new google.maps.Marker({
          map: map,
          icon: icon,
          title: place.name,
          position: place.geometry.location
        }));

        if (place.geometry.viewport) {
          // Only geocodes have viewport.
          bounds.union(place.geometry.viewport);
        } else {
          bounds.extend(place.geometry.location);
        }
      });
      map.fitBounds(bounds);
    });

}

let image = '/static/img/NewMarker1.gif'



function getPoints(map, infoWindow = infoWindow) {
    $.get('/incidents.json', function(incidents) {
        // debugger;
    let incident, marker, html;
        let markerArray = [];
    for (let key in incidents) {
        incident = incidents[key];
        incident.year = parseInt(incident.year)
        // if (incident.year === 2018) {
        //     image = '/static/img/Marker1.png'
        // };
        // if (incident.year === 2017) {
        //     image = '/static/img/Marker1.png'
        // };
        // if (incident.year === 2016) {
        //     image = '/static/img/Marker2.png'
        // };
        // if (incident.year === 2015) {
        //     image = '/static/img/Marker3.png'
        // };
        // if (incident.year === 2014) {
        //     image = '/static/img/Marker4.png'
        // };
        // if (incident.year === 2013) {
        //     image = '/static/img/Marker5.png'
        // };
        // if (incident.year === 2012) {
        //     image = '/static/img/Marker6.png'
        // };
        // if (incident.year === 2011) {
        //     image = '/static/img/Marker7.png'
        // };
        // if (incident.year === 2010) {
        //     image = '/static/img/Marker8.png'
        // };
        // if (incident.year === 2009) {
        //     image = '/static/img/Marker9.png'
        // };
        // if (incident.year === 2008) {
        //     image = '/static/img/Marker10.png'
        // };
        // if (incident.year === 2008) {
        //     image = '/static/img/Marker11.png'
        // };
        let icon = {
        url: image,
        scaledSize: new google.maps.Size(40, 50),
    }   
        // console.log(incident.latitude, incident.longitude)
        incident.latitude = parseFloat(incident.latitude);
        incident.longitude = parseFloat(incident.longitude);
        marker = new google.maps.Marker({
            // position: new google.maps.LatLng(incident.latitude, incident.longitude),
            // position : {lat: incident.latitiude, lng: incident.longitude},
            position : {lat: incident.latitude, lng: incident.longitude},
            map : map,
            title : 'Incident Type:' + incident.description,
            icon : icon
        });
        markerArray.push(marker);

        // console.log(incident);
        // console.log(incident.latitude, incident.longitude)
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
        bindInfo(marker, map, html, infoWindow = infoWindow);
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