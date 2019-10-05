const markerFillColor = '#f09e39';
const markerBorderColor = '#000000';

const markerStyle = `
  background-color: ${markerFillColor};
  border-radius: 50%;
  width: 1.5rem;
  height: 1.5rem;
  display: block;
  transform: rotate(45deg);
  border: 2px solid ${markerBorderColor}
`;

const icon = L.divIcon({
  className: 'my-custom-pin',
  iconAnchor: [20, 20],
  labelAnchor: [0, 0],
  popupAnchor: [-5, -30],
  html: `<span style="${markerStyle}" />
`,
});

var mymap = L.map('mapid', {
  attributionControl: false,
  zoomControl: false,
  zoomSnap: 0.25,
}).setView([20, 10], 1.5);

/* There are many, many map styles to choose from and
 * https://leaflet-extras.github.io/leaflet-providers/preview/
 * is a good way to see previews.
 *
 * The "default" map style is https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png
 *
 * See also:
 *
 * - https://wiki.openstreetmap.org/wiki/Tile_servers
 * - https://wiki.openstreetmap.org/wiki/Standard_tile_layer
 */
L.tileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/watercolor/{z}/{x}/{y}.{ext}', {
  maxZoom: 18,
  ext: 'jpg',
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(mymap);

L.control
  .zoom({
    position: 'bottomleft',
  })
  .addTo(mymap);

fetch('data/data.json')
  .then(function(response) {
    return response.json();
  })
  .then(function(myJson) {
    items = myJson.installations;
    document.getElementById("num-installations").innerHTML = items.length + " Installations";
    for (var i = 0; i < items.length; ++i) {
      name = items[i].name;
      hostname = items[i].hostname;
      linked_name =
        '<a target="_blank" rel="noopener noreferrer" href="http://' +
        hostname +
        '">' +
        name +
        '</a>';
      description = items[i].description;
      lat = items[i].lat;
      lng = items[i].lng;
      gdcc_member = items[i].gdcc_member;
      gdcc_member_note = '';
      if (gdcc_member) {
        gdcc_member_note =
          '<br><br><img src="images/gdcc-logo.png" width="20px"> <a target="_blank" rel="noopener noreferrer" href="http://dataversecommunity.global">Global Dataverse Community Consortium</a> member';
      }
      metrics_note = '';
      on_metrics = items[i].metrics;
      if (on_metrics) {
        metrics_note =
          '<br><br>Included in <a target="_blank" rel="noopener noreferrer" href="https://dataverse.org/metrics">dataverse.org/metrics</a>';
      }
      L.marker([lat, lng], { icon: icon })
        .addTo(mymap)
        .bindPopup(
          '<b>' + linked_name + '</b><br><br>' + description + gdcc_member_note + metrics_note,
        );
    }
  });
