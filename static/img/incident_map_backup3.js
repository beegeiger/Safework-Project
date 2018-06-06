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
        "saturation": 100
      },
      {
        "lightness": 95
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
        "color": "#0a00ff"
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
        "color": "#ffffff"
      },
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
        "color": "#2424e9"
      }
    ]
  },
  {
    "featureType": "landscape",
    "elementType": "geometry.fill",
    "stylers": [
      {
        "color": "#000000"
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
        "color": "#ad004c"
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
        "color": "#ff0000"
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
        "color": "#2424e9"
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
    initAutocomplete();
    return map;
}



// google.maps.event.addListener(searchBox , 'place_changed' , function(){
//     var searchBox = new google.maps.places.SearchBox(document.getElementById('pac-input'));
//     var places = searchBox.getPlaces();
//     var bounds =  new google.maps.LatLngBounds();
//     var i,place;
//     for( i = 0; place = places[i]; i++)
//     {
//     bounds.extend(place.geometry.location);
//     marker.setPosition(place.geometry.location);
//     }
//     map.fitBounds(bounds);
//     map.setZoom(12);
// }); 

function initAutocomplete() {
    var searchBox = new google.maps.places.SearchBox(document.getElementById('pac-input'));
    map.controls[google.maps.ControlPosition.TOP_CENTER].push(document.getElementById('pac-input'));
    google.maps.event.addListener(searchBox, 'places_changed', function() {
     searchBox.set('map', null);


     var places = searchBox.getPlaces();

     var bounds = new google.maps.LatLngBounds();
     var i, place;
     for (i = 0; place = places[i]; i++) {
       (function(place) {
         var marker = new google.maps.Marker({

           position: place.geometry.location
         });
         marker.bindTo('map', searchBox, 'map');
         google.maps.event.addListener(marker, 'map_changed', function() {
           if (!this.getMap()) {
             this.unbindAll();
           }
         });
         bounds.extend(place.geometry.location);


       }(place));

     }
     map.fitBounds(bounds);
     searchBox.set('map', map);
     map.setZoom(Math.min(map.getZoom(),12));

   });

google.maps.event.addDomListener(window, 'load', initAutocomplete);
}
//         // Create the search box and link it to the UI element.
//         var input = document.getElementById('pac-input');

//         var searchBox = new google.maps.places.SearchBox(input);
//         map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
//         var places = searchBox.getPlaces();
//         google.maps.event.trigger(input, 'focus')
//         google.maps.event.trigger(input, 'keydown', {keyCode:13})
//        searchBox.addListener('places_changed', function() {
//        if (places.length == 0) {
//          return;
//        }
// });


var image = '/static/img/Marker1.gif'
var num1 = 40
var num2 = 50
var opacity = 1.0

$(document).ready(function(){
  $( "#since2000" ).click(function(){
      if ($('#PointscheckBox').is(":checked")) {
        deleteMarkerGroup();
        changeMarkerGroup(class2000);
      }
      if ($('#HeatmapcheckBox').is(":checked")) {
        if (heatmap) {
          toggleHeatmap();
        }
        makeHeatMap(class2000heat);
      }
      console.log("2000 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2010" ).click(function(){
      if ($('#PointscheckBox').is(":checked")) {
        deleteMarkerGroup();
        changeMarkerGroup(class2010);
      }
      if ($('#HeatmapcheckBox').is(":checked")) {
        if (heatmap) {
          toggleHeatmap();
        }
        makeHeatMap(class2010heat);
      }
      console.log("2010 Button is working");
  });
});
$(document).ready(function(){
  $( "#since2017" ).click(function(){
      if ($('#PointscheckBox').is(":checked")) {
        deleteMarkerGroup();
        changeMarkerGroup(class2017);
      }
      if ($('#HeatmapcheckBox').is(":checked")) {
        if (heatmap) {
          toggleHeatmap();
        }
        makeHeatMap(class2017heat);
      }
      console.log("2017 Button is working");
  });
});



$(document).ready(function(){
  $( "#PointscheckBox" ).click(function(){
      if ($('#PointscheckBox').is(":checked")) {
          changeMarkerGroup(class2010);
      } else {
          deleteMarkerGroup();
      }
  });
});


$(document).ready(function(){
  $( "#HeatmapcheckBox" ).click(function(){
      if ($('#HeatmapcheckBox').is(":checked")) {
          makeHeatMap(class2010heat);
          styleHeatMap();
      } else {
          toggleHeatmap();
      }
  });
});



var year_class = []
var slide_val
var yearClass
var yearheat
$(document).ready(function(){
  $( "#year_slider" ).click(function(){
    slide_val = $( "#year_slider" ).val();
    console.log(slide_val)  
    console.log($('#PointscheckBox').is(":checked"))
    if ($('#PointscheckBox').is(":checked")) {  
      if (slide_val == 2000){
        yearClass = year2000;
      } else if (slide_val == 2001){
        yearClass = year2001;
      } else if (slide_val == 2002){
        yearClass = year2002;
      } else if (slide_val == 2003){
        yearClass = year2003;
      } else if (slide_val == 2004){
        yearClass = year2004;
      } else if (slide_val == 2005){
        yearClass = year2005;
      } else if (slide_val == 2006){
        yearClass = year2006;
      } else if (slide_val == 2007){
        yearClass = year2007;
      } else if (slide_val == 2008){
        yearClass = year2008;
      } else if (slide_val == 2009){
        yearClass = year2009;
      } else if (slide_val == 2010){
        yearClass = year2010;
      } else if (slide_val == 2011){
        yearClass = year2011;
      } else if (slide_val == 2012){
        yearClass = year2012;
      } else if (slide_val == 2013){
        yearClass = year2013;
      } else if (slide_val == 2014){
        yearClass = year2014;
      } else if (slide_val == 2015){
        yearClass = year2015;
      } else if (slide_val == 2016){
        yearClass = year2016;
      } else if (slide_val == 2017){
        yearClass = year2017;
      } else if (slide_val == 2018){
        yearClass = year2018;
      };
    deleteMarkerGroup();
    changeMarkerGroup(yearClass);
    console.log("Slider is working");
    };
    if ($('#HeatmapcheckBox').is(":checked")) {  
      if (slide_val == 2000){
        yearheat = year2000heat;
      } else if (slide_val == 2001){
        yearheat = year2001heat;
      } else if (slide_val == 2002){
        yearheat = year2002heat;
      } else if (slide_val == 2003){
        yearheat = year2003heat;
      } else if (slide_val == 2004){
        yearheat = year2004heat;
      } else if (slide_val == 2005){
        yearheat = year2005heat;
      } else if (slide_val == 2006){
        yearheat = year2006heat;
      } else if (slide_val == 2007){
        yearheat = year2007heat;
      } else if (slide_val == 2008){
        yearheat = year2008heat;
      } else if (slide_val == 2009){
        yearheat = year2009heat;
      } else if (slide_val == 2010){
        yearheat = year2010heat;
      } else if (slide_val == 2011){
        yearheat = year2011heat;
      } else if (slide_val == 2012){
        yearheat = year2012heat;
      } else if (slide_val == 2013){
        yearheat = year2013heat;
      } else if (slide_val == 2014){
        yearheat = year2014heat;
      } else if (slide_val == 2015){
        yearheat = year2015heat;
      } else if (slide_val == 2016){
        yearheat = year2016heat;
      } else if (slide_val == 2017){
        yearheat = year2017heat;
      } else if (slide_val == 2018){
        yearheat = year2018heat;
      };
    if (heatmap) {
       toggleHeatmap();
    }
    makeHeatMap(yearheat);
    styleHeatMap()
    }; 
  });
});

$(document).ready(function(){
  $( "#class_slider" ).click(function(){
    slide_val = $( "#class_slider" ).val();
    console.log(slide_val)  
    console.log($('#PointscheckBox').is(":checked"))
    if ($('#PointscheckBox').is(":checked")) {  
      if (slide_val == 1){
        yearClass = class2000;
      } else if (slide_val == 2){
        yearClass = class2010;
      } else if (slide_val == 3){
        yearClass = class2017;
      };
    deleteMarkerGroup();
    changeMarkerGroup(yearClass);
    console.log("Slider is working");
    };
    if ($('#HeatmapcheckBox').is(":checked")) {  
      if (slide_val == 1){
        yearheat = class2000heat;
      } else if (slide_val == 2){
        yearheat = class2010heat;
      } else if (slide_val == 3){
        yearheat = class2017heat;
      };
    if (heatmap) {
       toggleHeatmap();
    }
    makeHeatMap(yearheat);
    styleHeatMap()
    }; 
  });
});






var incident
var incidents
var markersArray = []


function deleteMarkerGroup() {
  // console.log(markArr)
  for (var i = 0; i < markArr.length; i++ ) {
    markArr[i].setMap(null);
} markArr=[];
  markArr.length = 0;
}
function changeMarkerGroup(group) {
  var infowindow = new google.maps.InfoWindow({
        });
  console.log("cMS was called")
  markArr = group;
  markArr.length = group.length;
  for (var j = 0 ; j < group.length; j++) {
   
   markArr[j].setMap(map);
   bindInfo(markArr[j], markArr[j].html, infowindow);    
  }

}


function bindInfo(marker, html, infowindow) {
    google.maps.event.addListener(marker, 'click', function () {
        infowindow.close();
        infowindow.setContent(html)
        infowindow.open(map, marker);
        });
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
        marker = new google.maps.Marker({
            position : {lat: incident.latitude, lng: incident.longitude},
            title : 'Incident Type:' + incident.description,
            icon : icon,
            year: incident.year,
            lat: incident.lat,
            long: incident.long
        });
        marker.lat = incident.latitude
        marker.long = incident.longitude
        // bindInfo(marker, html, infoWindow);
        
        // window.incident = incident;
        marker.html = ((
          '<div class="' + incident.year + '" >' +
                '<p><b>'+ incident.description +'</b></p>' +
                '<p><b>'+ incident.incident_id +'</b></p>' +
                '<p><b>Address: </b>' + incident.address + '</p>' +
                '<p><b>City: </b>' + incident.city + '</p>' +
                '<p><b>State: </b>' + incident.state + '</p>' +
                '<p><b>Date: </b>' + incident.date + '</p>' +
                '<p><b>Time: </b>' + incident.time + '</p>' +
                '<p><b>Police Record Number: </b>' + incident.rec_number + '</p>' +
              '</div>'));
        markArr.push(marker);
        };
        console.log(markArr[1].year)
        console.log(markArr[1].lat)        
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

var year2000heat = []
var year2001heat = []
var year2002heat = []
var year2003heat = []
var year2004heat = []
var year2005heat = []
var year2006heat = []
var year2007heat = []
var year2008heat = []
var year2009heat = []
var year2010heat = []
var year2011heat = []
var year2012heat = []
var year2013heat = []
var year2014heat = []
var year2015heat = []
var year2016heat = []
var year2017heat = []
var year2018heat = []
var class2000heat = []
var class2010heat = []
var class2017heat = []

var marker

function makeMarkerGroups(markArr) {
  // console.log(markArr)
  console.log(markArr[1].year)
  for (var h=0; h < markArr.length; h++) {
      marker = markArr[h];
      if (marker.year == 2000) {
      year2000.push(marker);
      class2000.push(marker);
      year2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2001) {
      year2001.push(marker);
      class2000.push(marker);
      year2001heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2002) {
      year2002.push(marker);
      class2000.push(marker);
      year2002heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2003) {
      year2003.push(marker);
      class2000.push(marker);
      year2003heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2004) {
      year2004.push(marker);
      class2000.push(marker);
      year2004heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2005) {
      year2005.push(marker);
      class2000.push(marker);
      year2005heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2006) {
      year2006.push(marker);
      class2000.push(marker);
      year2006heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2007) {
      year2007.push(marker);
      class2000.push(marker);
      year2007heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2008) {
      year2008.push(marker);
      class2000.push(marker);
      year2008heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2009) {
      year2009.push(marker);
      class2000.push(marker);
      year2009heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2010) {
      year2010.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2011) {
      year2011.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2011heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if(marker.year == 2012) {
      year2012.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2012heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2013) {
      year2013.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2013heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2014) {
      year2014.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2014heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2015) {
      year2015.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2015heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if (marker.year == 2016) {
      year2016.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      year2016heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if(marker.year == 2017) {
      year2017.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      class2017.push(marker);
      year2017heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2017heat.push(new google.maps.LatLng(marker.lat, marker.long));
    } else if(marker.year == 2018) {
      console.log("2018 should be working!")
      year2018.push(marker);
      class2000.push(marker);
      class2010.push(marker);
      class2017.push(marker);
      // console.log(marker.year)
      // console.log(marker.lat)
      // console.log(typeof marker.lat)
      year2018heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2000heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2010heat.push(new google.maps.LatLng(marker.lat, marker.long));
      class2017heat.push(new google.maps.LatLng(marker.lat, marker.long));

    };

  }
  console.log("Should be calling changeMarkerGroup")  
  changeMarkerGroup(class2010);
  makeHeatMap(class2010heat);
  styleHeatMap(); 
}

var heatmap

function makeHeatMap(data) {
  heatmap = new google.maps.visualization.HeatmapLayer({
  data: data,
  map: map})
  console.log("makeHeatMap Called")
}

function styleHeatMap(){
  changeGradient();
  changeRadius();
  changeOpacity();
}


function toggleHeatmap() {
  heatmap.setMap(heatmap.getMap() ? null : map);
}

function changeGradient() {
  var gradient = [
  "rgba(102, 255, 0, 0)",
  "rgba(147, 255, 0, 1)",
  "rgba(193, 255, 0, 1)",
  "rgba(244, 227, 0, 1)",
  "rgba(249, 198, 0, 1)",
  "rgba(255, 170, 0, 1)",
  "rgba(255, 113, 0, 1)",  
  "rgba(255, 113, 0, 1)",
  "rgba(255, 57, 0, 1)",
  "rgba(255, 57, 0, 1)",
  "rgba(255, 0, 0, 1)",
  "rgba(255, 0, 0, 1)",
  "rgba(255, 0, 0, 1)",
  "rgba(255, 0, 0, 1)"
  ]
  heatmap.set('gradient', heatmap.get('gradient') ? null : gradient);
}

function changeRadius() {
  heatmap.set('radius', heatmap.get('radius') ? null : 50);
}

function changeOpacity() {
  heatmap.set('opacity', heatmap.get('opacity') ? null : 1);
}
