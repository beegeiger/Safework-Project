$('#all-selectors').change(function () {
  console.dir($('#slide_but'))
  console.dir($('#year_slider').val())
  console.dir($('#since2000'))
  console.dir($('#since2010'))
  console.dir($('#since2017'))

    let formInputs = {'sliderYear': $('#year_slider').val(),
        "since2000": $('#since2000').val(),
        "since2010": $('#since2010').val(),
        "since2017": $('#since2017').val(),
}

	 $.get('/incidents.json', formInputs, initLoadmarkers)