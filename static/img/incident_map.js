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
var allMarkers = {}
var Mar = []
var happy = [1,2,3]
var markArr = []

function initMap() {
    map = get_map();
    get_infoWindow();
    getPoints();
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

var image = '/static/img/Marker1.gif'
var num1 = 40
var num2 = 50
var opacity = 1.0

$(document).ready(function(){
  $( "#since2000" ).click(function(){
      changeMarkerGroup(empty);
      console.log("2000 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2010" ).click(function(){
      deleteMarkerGroup();
      console.log("2010 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2017" ).click(function(){
      changeMarkerGroup(class2017);
      console.log("2017 Button is working");
  });
});
 var empty = []

var incident
var incidents
var markersArray = []
var mark

function deleteMarkerGroup() {
  console.log(markArr)
  for (var i = 0; i < markArr.length; i++ ) {
    // markArr[i].setMap(null);
    // markArr[i].setMap(map);
  }
}

function changeMarkerGroup(group) {
  markArr = group;
  markArr.length = group.length;
  for (var j = 0 ; j < group.length; j++) {
    marker = markArr[j];
    mark = new google.maps.Marker({
        position : marker.position,
        map : marker.map,
        title : marker.title2,
        icon : marker.icon,
    });
  }
  console.log(markArr)

}




function getPoints() {
    $.get('/incidents.json', function(incidents) {
        // debugger;
    let incident, marker, html;
        let markArr = [];
        let year_class = "";

    for (let key in incidents) {
        incident = incidents[key];
        incident.year = parseInt(incident.year);
        if (incident.year >= 2017) {
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
        marker = {
            position : {lat: incident.latitude, lng: incident.longitude},
            map : map,
            title2 : 'Incident Type:' + incident.description,
            icon : icon,
            year: incident.year,
            description: incident.description,
            incident_id: incident.incident_id,
            address: incident.address,
            city: incident.city,
            state: incident.state,
            date: incident.date,
            time: incident.time,
            rec_number: incident.rec_number
        };
        // bindInfo(marker, html, infoWindow);
        markArr.push(marker);
        // window.incident = incident;
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
        };
        console.log(markArr)
        console.log(markArr[1].year)        
        makeMarkerGroups(markArr); 
    });
}


function removeMarkers(){
    console.log("Should be clearing markers")
    for(incident=0; incident<markers.length; incident++){
        markers[i].setMap(null);
    }
}

// Sets the map on all markers in the array.
function setMapOnAll(map, markers) {
  for (incident = 0; incident < markers.length; incident++) {
    markers[incident].setMap(map);
  }
}

function bindInfo(marker, html, infoWindow) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.close();
        infoWindow.setContent(html);
        infoWindow.open(marker);
        });
}

var year2000 = []
var year2001 = []
var year2002 = []
var year2003 = []
var year2004 = []
var year2005 = []
var year2006 = []
var year2007 = []
var year2008 = []
var year2009 = []
var year2010 = []
var year2011 = []
var year2012 = []
var year2013 = []
var year2014 = []
var year2015 = []
var year2016 = []
var year2017 = []
var year2018 = []
var class2000 = []
var class2010 = []
var class2017 = []


var marker

function makeMarkerGroups(markArr) {
  console.log(markArr)
  console.log(markArr[1].year)
  for (var h=0; h < markArr.length; h++) {
      marker = markArr[h];
      // console.log(marker)
      if (marker.year == 2000) {
      year2000.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2001) {
      year2001.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2002) {
      year2002.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2003) {
      year2003.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2004) {
      year2004.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2005) {
      year2005.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2006) {
      year2006.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2007) {
      year2007.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2008) {
      year2008.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2009) {
      year2009.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2010) {
      year2010.push(marker);
      class2000.push(marker);
    } else if (marker.year == 2011) {
      year2011.push(marker);
      class2000.push(marker);
      class2010.push(marker);
    } else if (marker.year == 2012) {
      year2012.push(marker);
      class2000.push(marker);
      class2010.push(marker);
    } else if (marker.year == 2013) {
      year2013.push(marker);
      class2000.push(marker);
      class2010.push(marker);
    } else if (marker.year == 2014) {
      year2014.push(marker);
      class2000.push(marker);
      class2010.push(marker);
    } else if (marker.year == 2015) {
      year2015.push(marker);
      class2000.push(marker);
      class2010.push(marker);
    } else if (marker.year == 2016) {
      year2016.push(marker);
      class2000.push(marker);
      class2010.push(marker);
    } else if (marker.year == 2017) {
      year2017.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      class2017.push(marker);
    } else if (marker.year == 2018) {
      console.log("2018 should be working!")
      year2018.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      class2017.push(marker);
    }; 
  }
}
