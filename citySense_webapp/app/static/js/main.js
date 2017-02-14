$(document).ready(function() {

    /*=======================================
	parameter constants
	=======================================*/

	var api_url = '/get_last_item_sensor/';
    var map; 
    var window_timer = 60 * 1 * 1000; //1 minute;
    var default_sensor = "01"; 

    /*=======================================
	map
	=======================================*/

    function init_map(){
    	map = L.map('map', {zoomControl: false}).setView([25.28, 51.53], 12);

		L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiYSI6ImNpandmbXliNDBjZWd2M2x6bDk3c2ZtOTkifQ._QA7i5Mpkd_m30IGElHziw', {
		    maxZoom: 18,
		    attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, ' +
		        '<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
		        'Imagery © <a href="http://mapbox.com">Mapbox</a>',
		    id: 'mapbox.light'
		}).addTo(map);

		/* I should be reading it from database. I have one sensor.*/
		var sensors_geojson = {
	    "type": "Feature",
	    "properties": {
	        "sensor_id": "01"
	    },
		    "geometry": {
		        "type": "Point",
		        "coordinates": [51.53, 25.38]
		    }
		};

		var sensors_geojson_style = {
		    "radius": 8,
		    "fillColor": "#ff7800",
		    "color": "#000",
		    "weight": 1,
		    "opacity": 1,
		    "fillOpacity": 0.8
		};

		L.geoJSON(sensors_geojson, {

        	onEachFeature: onEachFeature, 
		    pointToLayer: function (feature, latlng) {
		        return L.circleMarker(latlng, sensors_geojson_style);
		    }
		}).addTo(map);


	}


	/*=======================================
    helpful functions to get catch zone information
    =======================================*/

    function onEachFeature(feature, layer) {

	    if (feature.properties && feature.properties.sensor_id) {
	        layer.bindPopup("Sensor ID:" + feature.properties.sensor_id);
	    }

        layer.on({
            click: sensor_clicker
        });
    }


    function sensor_clicker(e) {
        var sensor_id = e.target.feature.properties.sensor_id;
        launch_citysense(api_url+sensor_id);

    }

	/*=======================================
	functions to update fields in the page
	=======================================*/
    function update_temperature_value(value) {
        $('#temperature_value').text(value);
    }
    
    function update_humidity_value(value) {
        $('#humidity_value').text(value);
    }
    
    function update_co2_value(value) {
        $('#co2_value').text(value);
    }

    function update_crowd_value(value) {
        $('#crowd_value').text(value);
    }

    function update_pressure_value(value) {
        $('#pressure_value').text(value);
    }

    function update_light_value(value) {
        $('#light_value').text(value);
    }

    function update_noise_value(value) {
        $('#noise_value').text(value);
    }

	/*=======================================
	functions to update fields in the page

	the data that we get from server represented this way:
	data = {
			temperature:,
			humidity:,
			co2:,
			crowd:,
			pressure:,
			light:,
			noise:, 
		}
	=======================================*/

	function get_citysense_data(data){
		update_temperature_value(data.temperature);
		update_humidity_value(data.humidity);
		update_co2_value(data.co2);
		update_crowd_value(data.crowd); 
    }

	function update_citysense(api_url){

		setInterval(function() {

	    $.getJSON(api_url, function(data, responseText, jqXHR) {

	            if (jqXHR.status != 204) {
	                if (jqXHR.status != 204) {

	                	console.log(data);
	                	get_citysense_data(data)

	   
	                }
	            }
	    });

		}, window_timer);
    }

    function launch_citysense(api_url){

    	 $.getJSON(api_url, function(data, responseText, jqXHR) {

	            if (jqXHR.status != 204) {
	                if (jqXHR.status != 204) {

	                	console.log(data);
	                	get_citysense_data(data)

	   
	                }
	            }
	    });

    }

	/*=======================================
	main
	=======================================*/


    init_map();
    launch_citysense(api_url+default_sensor);
    update_citysense(api_url+default_sensor);

});