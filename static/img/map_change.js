function deleteMarkers() {
        markers.setMap(null);
      }
// $('#all-selectors').change(function () {
//   console.log("Something is happening!")
//   console.dir($('#slide_but'))
//   console.dir($('#year_slider').val())
//   console.dir($('#since2000'))
//   console.dir($('#since2010'))
//   console.dir($('#since2017'))

//     let formInputs = {'sliderYear': $('#year_slider').val(),
//         "since2000": $('#since2000').val(),
//         "since2010": $('#since2010').val(),
//         "since2017": $('#since2017').val(),
// }
// });
// $(document).ready(function(){
//   $( "#slide_but" ).click(function(){
//       initLoadSliderMarkers(formInputs, 2018);
//       console.log("Slide Button is working");
//   });
// });
// $(document).ready(function(){
//   $( "#year_slider" ).click(function(){
//       initLoadSliderMarkers(formInputs, formInputs['sliderYear']);
//       console.log("Slide Button is working");
//   });
// });
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

// $('#since2000').addEventListener('click', function(){
//     console.log("2000 Button is working");
// });


// $('#since2010').addEventListener('click', function(){
//     initLoadGroupMarkers(this.value);
//     console.log("2010 Button is working");
// });


// $('#since2017').addEventListener('click', function(){
//     initLoadGroupMarkers(this.value);
//     console.log("2017 Button is working");
// });


// $( "#since2000" ).onClick(function(){
//     initLoadGroupMarkers(this.value);
//     console.log("2000 Button is working");
// });


// $( "#since2010" ).onClick(function(){
//     initLoadGroupMarkers(this.value);
//     console.log("2010 Button is working");
// });


// $( "#since2017" ).onClick(function(){
//     initLoadGroupMarkers(this.value);
//     console.log("2017 Button is working");
// });



let formInputs = {'sliderYear': $('#year_slider').val(),
      "since2000": $('#since2000').val(),
      "since2010": $('#since2010').val(),
      "since2017": $('#since2017').val(),
}

function initLoadGroupMarkers(years) {
  $.get('/incidents.json', function(incidents, years=years) {


  console.log("Changing Markers")
  let incident, marker, html;
  let infoWindow = new google.maps.InfoWindow({});
  let markers = [];
  for (let key in incidents) {
    incident = incidents[key];
    incident.year = parseInt(incident.year);
    if (incident.year >= 2017 && years == 2017) {
        image = '/static/img/Marker1.gif';
        num1 = 45;
        num2 = 60;
        opacity = 1.0;
    } else if (incident.year > 2016 && years != 2017) {
        image = '/static/img/Marker2.gif';
        num1 = 43;
        num2 = 57;
        opacity = 0.95;
    } else if (incident.year > 2015 && years != 2017) {
        image = '/static/img/Marker3.gif';
        num1 = 40;
        num2 = 53;
        opacity = 0.9;
    } else if (incident.year > 2014 && years != 2017) {
        image = '/static/img/Marker4.gif';
        num1 = 37;
        num2 = 50;
        opacity = 0.85;
    } else if (incident.year > 2012 && years != 2017) {
        image = '/static/img/Marker5.gif';
        num1 = 33;
        num2 = 45;
        opacity = 0.8;
    } else if (incident.year > 2010 && years != 2017) {
        image = '/static/img/Marker6.gif';
        num1 = 30;
        num2 = 40;
        opacity = 0.7;
    } else if (incident.year > 2008 && years == 2000) {
        image = '/static/img/Marker7.gif';
        num1 = 26;
        num2 = 35;
        opacity = 0.6;
    } else if (incident.year > 2005 && years == 2000) {
        image = '/static/img/Marker8.gif';
        num1 = 22;
        num2 = 30;
        opacity = 0.5;
    } else if (incident.year > 2002 && years == 2000) {
        image = '/static/img/Marker9.gif';
        num1 = 18;
        num2 = 25;
        opacity = 0.4;
    } else if (years == 2000) {
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
    bindInfo(marker, map, html, infoWindow = infoWindow);
    markers.push(marker);
}
    marker_layer = new google.maps.Data({
    data: markers,
    });
});
}  

function bindInfo(marker, html, infoWindow) {
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.close();
        infoWindow.setContent(html);
        infoWindow.open( marker);
        });
}
