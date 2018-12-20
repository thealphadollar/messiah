// will use variable searchQuery, previously
// fetched from GET parameters

// OpenStreetMap imagery, OpenStreetMap Nominatim for Geocoding
const tileProviderUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
const geocodingUrl = 'https://nominatim.openstreetmap.org/search?format=json&q=';
const mapId = 'my_map_add';

// make map global for use in other places
var map;

/**
 * Creates a Leaflet map 
 * @param {String} mapId must include the id of the div where map will be placed
 * @param {*} place must include the following attributes 'latlong' (array), 'importance' (float), 'name' (string)
 */
function createMap(mapId, place) {
    var zoomLevel = 5 + (6 * (1 - place.importance)); // zoom level on the basis of importance of place

    map = L.map(mapId).setView(place.latlong, zoomLevel);
    L.tileLayer(tileProviderUrl, {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // marker at the location
    L.marker(place.latlong).addTo(map)
        .bindPopup('<b>' + place.name + '</b><br>This is the place that<br>you are looking for.')
        .openPopup();
}

/**
 * Get the geo coordinates of a place
 * plus, create a map of the given place using createMap
 * @param {*} placeName name of the place / search query to geocode
 */
/*function geocodePlace(placeName) {
    searchQuery = "India";
    var reqdPlace = {
        latlong: [], importance: 0.0, name: ''
    };

    var requestUrl = geocodingUrl + placeName;
    var request = new XMLHttpRequest();
    request.addEventListener('readystatechange', function() {
        if(this.status == 200 && this.readyState == 4) {
            var resObj = JSON.parse(this.responseText);
            reqdPlace.latlong = [resObj[0].lat, resObj[0].lon];
            reqdPlace.importance = resObj[0].importance;
            reqdPlace.name = resObj[0].display_name;

            createMap(mapId, reqdPlace);
        }
    })
    request.open('GET', requestUrl);
    request.send();
}*/
function geocodePlace(splitLink) {
    placeName = "India";
    var reqdPlace = {
        latlong: [], importance: 0.0, name: ''
    };
	if(splitLink.length>1){
			if(splitLink[2]!=null)
				placeName = splitLink[2];
			else
				placeName = splitLink[1].replace(/%20/g, " ");
	}
			var requestUrl = geocodingUrl + placeName;
		    var request = new XMLHttpRequest();
		    request.addEventListener('readystatechange', function() {
			if(this.status == 200 && this.readyState == 4) {
			    var resObj = JSON.parse(this.responseText);
			    //reqdPlace.latlong = [splitLink[3],splitLink[4]];
			    reqdPlace.latlong = [resObj[0].lat, resObj[0].lon];				
			    reqdPlace.importance = resObj[0].importance;
			    reqdPlace.name = resObj[0].display_name;

                createMap(mapId, reqdPlace);
                // mark relief centers
                markReliefCenters();
			}
		    })
		    request.open('GET', requestUrl);
		    request.send();		   
}
geocodePlace(splitLink);
