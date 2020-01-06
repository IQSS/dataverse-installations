const markerFillColor = '#C55B28';
const markerBorderColor = '#FFFFFF';

const markerStyle = `
  background-color: ${markerFillColor};
  border-radius: 50%;
  width: 0.6rem;
  height: 0.6rem;
  display: block;
  transform: rotate(45deg);
  border: 1px solid ${markerBorderColor}
`;

const icon = L.divIcon({
  className: 'my-custom-pin',
  iconAnchor: [5, 5],
  labelAnchor: [0, 0],
  popupAnchor: [1, -10],
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
L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 19
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
    document.getElementById('num-installations').innerHTML = items.length + ' Installations';
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
      about_url = items[i].about_url;
      about_url_note = '';
      if (about_url) {
        about_url_note =
          ' <a target="_blank" rel="noopener noreferrer" href="' + about_url + '">More...</a>';
      }
      lat = items[i].lat;
      lng = items[i].lng;
      launch_year = items[i].launch_year;
      launch_year_note = '';
      if (launch_year) {
        launch_year_note = '<br><br>Launched in ' + launch_year;
      }
      core_trust_seals = items[i].core_trust_seals;
      core_trust_seal_note = '';
      if (core_trust_seals) {
        seal_urls = [];
        for (var j = 0; j < core_trust_seals.length; ++j) {
          seal_url = core_trust_seals[j];
          link =
            '<a target="_blank" rel="noopener noreferrer" href="' +
            seal_url +
            '"><img src="images/coretrustseal.jpg" width="20px"></a>';
          seal_urls.push(link);
        }
        core_trust_seal_note = '<br><br>CoreTrustSeal certifications: ' + seal_urls.join(' ');
      }
      board = items[i].board;
      board_note = '';
      if (board) {
        board_note =
          '<br><br><a target="_blank" rel="noopener noreferrer" href="' +
          board +
          '">Project board</a>';
      }
      harvesting_sets = items[i].harvesting_sets;
      harvesting_note = '';
      if (harvesting_sets) {
        set_names = [];
        for (var j = 0; j < harvesting_sets.length; ++j) {
          set_name = harvesting_sets[j];
          set_names.push(set_name);
        }
        //harvesting_note = '<br><br>Harvesting sets: ' + harvesting_sets.length;
        list_sets_url = 'http://' + hostname + '/oai?verb=ListSets';
        harvesting_note =
          '<br><br>Advertised ' +
          '<a target="_blank" rel="noopener noreferrer" href="' +
          list_sets_url +
          '">harvesting sets</a>: ' +
          set_names.join(', ');
      }
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
          '<b>' +
            linked_name +
            '</b><br><br>' +
            description +
            about_url_note +
            core_trust_seal_note +
            harvesting_note +
            launch_year_note +
            board_note +
            gdcc_member_note +
            metrics_note,
        );
    }
  });
