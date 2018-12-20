



// will use variables map from global code
// use LeafletJS and OSM Overpass API
// to mark relief centers near a searchRadius
// of the map center

// OverPass API for querying OSM Data using Overpass QL
const overpassURL = 'http://overpass-api.de/api/interpreter?data=';

/**
 * Function will convert OSM nodes data
 * into suitable form such that it can be 
 * mapped with Leaflet with the help of simple markers
 * (only nodes, no relations / ways)
 * @param {*} osmDataObject Parsed object from OSM data collected as JSON
 */

function markersFromOsmData(osmDataObject) {
    var markers = [];
    var nodes = osmDataObject['elements'];
    for(var index = 0; index < nodes.length; index++) {
        var marker = {
            lat: nodes[index]['lat'], 
            lon: nodes[index]['lon'],
            link: 'https://openstreetmap.org/node/' + nodes[index]['id']
        }
        // name if present
        if(nodes[index].tags['name'] != undefined) {
            marker.name = nodes[index].tags['name'];
        }
        markers.push(marker);
    }
    return markers;
}

/**
 * Function will plot the markers on the 
 * Leaflet Map using the marker data that's parsed
 * @param {*} markers must include an array of marker related data with fields lat, lon, link and (optional) names
 */
function plotMarkers(markers) {
    // use a custom icon
    var rIcon = L.icon({
        iconUrl: '/img/rlogo.png',
        iconSize: [30, 30],
        iconAnchor: [15, 15]
    });
    for(var index = 0; index < markers.length; index++) {
        var message = '<b>' + ((markers[index].name !== undefined) ? markers[index].name : "") + '</b><br>This maybe a nearby relief center.<br>More information about this place may be available <a href="' + markers[index].link + '" target="_blank">here</a>.';
        console.log(message)
        L.marker([markers[index]['lat'], markers[index]['lon']], {icon: rIcon}).addTo(map)
            .bindPopup(message);
    }
}

/**
 * Function marks nearby relief centers
 * based on map center,
 * on given Leaflet Map
 */
function markReliefCenters() {

    const searchRadius = 10000; // in m, set to 10km
    // lat long of the map center
    const around = [
        searchRadius,
        map.getCenter()['lat'], 
        map.getCenter()['lng']
    ].join(',');

    // Overpass QL code to get list
    // of nearby hospitals / clinics / admin boundaries (govt) / municipality
    // as relief centers around searchRadius
    const qlCode = '[out:json];node(around:' + around + ')[~"amenity|boundary|place"~"hospital|clinic|government|municipality|administrative"];out;';

    // map the OSM data object after an AJAX request to the Overpass API
    var anotherRequest = new XMLHttpRequest();
    anotherRequest.addEventListener('readystatechange', function() {
        if(this.status == 200 && this.readyState == 4) {
            var osmObject = JSON.parse(this.responseText);
            var reqdMarkers = markersFromOsmData(osmObject);
            console.log(reqdMarkers);
            plotMarkers(reqdMarkers);
        }
    });
    console.log('Request is being made to: "' + overpassURL + qlCode + '"');
    anotherRequest.open('GET', overpassURL + qlCode);
    anotherRequest.send();
}