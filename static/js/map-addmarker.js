var currentMarker;
var lat;
var lng;

function getAndSetCoordinates(event) {
    // to update hidden form fields
    lat = event.latlng.lat;
    lng = event.latlng.lng;
    document.getElementById('id_latitude').value = lat;
    document.getElementById('id_longitude').value = lng;
}

map.on("click", function (event) {
    // marker already added, allow repositioning
    if (currentMarker) {
        currentMarker.setLatLng(event.latlng);
        getAndSetCoordinates(event)
        return;
    }
    
    // marker not yet added, allow only one to be added
    currentMarker = L.marker(event.latlng, {
    }).addTo(map).on("click", function () {
        event.originalEvent.stopPropagation();
    });
    
    getAndSetCoordinates(event)
});
