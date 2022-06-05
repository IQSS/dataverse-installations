let url = 'data/data.json';
let byYear = {};
let years = [];
fetch(url).then(function(response) {
  response.text().then(function(text) {
    obj = JSON.parse(text);
    installations = obj.installations;
    https: for (const installation of installations) {
      let launch_year = installation.launch_year;
      if (launch_year == undefined) {
        launch_year = '????';
      }
      if (byYear[launch_year] == undefined) {
        byYear[launch_year] = [];
      }
      byYear[launch_year].push(installation.name);
    }
    var div = document.getElementById('yearid');
    div.innerHTML += 'Dataverse Installations by Year\n';
    for (const [key, value] of Object.entries(byYear)) {
      let stars = '';
      for (installation of value) {
        stars += '*';
      }
      div.innerHTML += `${key} ` + stars + ` ${value.length}` + '\n';
    }
    div.innerHTML += '\n';
    div.innerHTML += 'Dataverse Installations by Over Time\n';
    let runningTotal = 0;
    for (const [year, installations] of Object.entries(byYear)) {
      runningTotal += installations.length;
      let stars = '';
      for (let i = 0; i < runningTotal; i++) {
        stars += '*';
      }
      div.innerHTML += `${year} ${stars} ${runningTotal}\n`;
    }
    if (byYear['????'].length > 0) {
      div.innerHTML += '\nInstallations with Unknown Launch Year\n';
      for (const unknown of byYear['????']) {
        div.innerHTML += unknown + '\n';
      }
    }
  });
});
