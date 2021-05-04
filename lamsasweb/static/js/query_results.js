$(document).ready( function () {
    $('#results_table').DataTable({
        ordering: false
    });
});

if (map == true){
  var mymap = L.map('mapid').setView([38, -97], 4);
  var marker = null;
  L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox/streets-v11', //mapbox/streets-v11 mapbox/satellite-v9
      tileSize: 512,
      zoomOffset: -1,
      accessToken: 'pk.eyJ1IjoibnlhbmJpbmFyeSIsImEiOiJja2tyZHRpb3YzZHRsMnFwZGh4czFvMXExIn0.XvfoTg3nfGCBDU0Vs-LBBw'
  }).addTo(mymap);
}

function updateMap(lat, long, maplink) {
  if (marker !== null) {
    marker.remove()
  }
  mymap.setView([lat, long], 13);
  marker = L.marker([lat, long]);
  marker.addTo(mymap);
  marker.bindPopup("Current Location:<br>"+lat+'°N, '+long+'°E').openPopup();
}

function toggleMapVisibility() {
  var mapdiv = document.getElementById('mapid');
  var hidemaptext = document.getElementById('hidemap');
  mapdiv.hidden = !mapdiv.hidden;
  if (mapdiv.hidden == true) {
    hidemaptext.text = 'Show Map';
  } else {
    hidemaptext.text = 'Hide Map';
  }
}
