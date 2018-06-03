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
var map
var infoWindow
var markers

function initMap() {
    map = get_map();
    get_infoWindow();
    // getPoints("2010");
}

function get_infoWindow() {
  return infoWindow = new google.maps.InfoWindow({});
}

function get_map() {
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
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.772121, lng: -122.420850},
        zoom: 13
    });
    map.mapTypes.set('styled_map', styledMapType);
    map.setMapTypeId('styled_map');
    return map;
}
var markers =[]
var image = '/static/img/Marker1.gif'
var num1 = 40
var num2 = 50
var opacity = 1.0

$(document).ready(function(){
  $( "#since2000" ).click(function(){
      getPoints("2000");
      console.log("2000 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2010" ).click(function(){
      getPoints("2010");
      console.log("2010 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2017" ).click(function(){
      getPoints("2017");
      console.log("2017 Button is working");
  });
});

function setMapOnAll(map, markers) {
        for (var i = 0; i < markers.length; i++) {
          markers[i].setMap(map);
        }
      }

function deleteMarkers() {
    setMapOnAll(null);
    markers = [];
}

function getPoints(yearClass) {
    $.get('/incidents.json', function(incidents) {
        // debugger;

    let incident, marker, html;
    infoWindow = get_infoWindow();
    markers = [];
    for (let key in incidents) {
        incident = incidents[key];
        incident.year = parseInt(incident.year);
        if (incident.year >= 2017 && yearClass == "2017") {
            image = '/static/img/Marker1.gif';
            num1 = 45;
            num2 = 60;
            opacity = 1.0;
        } else if (incident.year > 2016 && yearClass != "2017") {
            image = '/static/img/Marker2.gif';
            num1 = 43;
            num2 = 57;
            opacity = 0.95;
        } else if (incident.year > 2015 && yearClass != "2017") {
            image = '/static/img/Marker3.gif';
            num1 = 40;
            num2 = 53;
            opacity = 0.9;
        } else if (incident.year > 2014 && yearClass != "2017") {
            image = '/static/img/Marker4.gif';
            num1 = 37;
            num2 = 50;
            opacity = 0.85;
        } else if (incident.year > 2012 && yearClass != "2017") {
            image = '/static/img/Marker5.gif';
            num1 = 33;
            num2 = 45;
            opacity = 0.8;
        } else if (incident.year > 2010 && yearClass != "2017") {
            image = '/static/img/Marker6.gif';
            num1 = 30;
            num2 = 40;
            opacity = 0.7;
        } else if (incident.year > 2008 && yearClass == "2000") {
            image = '/static/img/Marker7.gif';
            num1 = 26;
            num2 = 35;
            opacity = 0.6;
        } else if (incident.year > 2005 && yearClass == "2000") {
            image = '/static/img/Marker8.gif';
            num1 = 22;
            num2 = 30;
            opacity = 0.5;
        } else if (incident.year > 2002 && yearClass == "2000") {
            image = '/static/img/Marker9.gif';
            num1 = 18;
            num2 = 25;
            opacity = 0.4;
        } else if (yearClass == "2000") {
            image = '/static/img/Marker10.gif';
            num1 = 15;
            num2 = 20;
            opacity = 0.3;
        } else {
            incident = []
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
        bindInfo(marker, html, infoWindow);
        setMapOnAll(map, markers);
        };
    });
}




function bindInfo(marker, html, infoWindow) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.close();
        infoWindow.setContent(html);
        infoWindow.open(marker);
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