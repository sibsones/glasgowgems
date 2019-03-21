// default map view of Glasgow
var map = L.map('mapid').setView([55.850, -4.235], 11);

L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiMjMzMDk5NGIiLCJhIjoiY2pzbmNxdGFnMDl0MTQzanZtcTAybmlmbiJ9.b2a_gM6iUQjU_kYH30K6Bw', {
    maxZoom: 18,
    attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, ' +
        '<a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, ' +
        'Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
    id: 'mapbox.streets'
}).addTo(map);
