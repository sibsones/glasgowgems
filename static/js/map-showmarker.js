// marker added to the map based on values from gemLatitude and gemLongitude template tags
var newMarker = new L.marker([gemLatitude, gemLongitude], {
    title: gemName, alt: gemName
}).addTo(map);
