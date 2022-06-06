// inspired by https://codepen.io/Muthukrishnan/pen/vGoZVz
let url = "data/data.json";

fetch(url).then(function (response) {
  response.text().then(function (text) {
    var byYear = {};
    var byYearData = [];
    var overTimeData = [];

    obj = JSON.parse(text);
    installations = obj.installations;

    https: for (const installation of installations) {
      let launch_year = installation.launch_year;
      if (byYear[launch_year] == undefined) {
        byYear[launch_year] = [];
      }
      byYear[launch_year].push(installation.name);
    }

    let runningTotal = 0;
    for (const [year, installations] of Object.entries(byYear)) {
      let countByYear = {};
      countByYear["year"] = year;
      countByYear["count"] = installations.length;
      byYearData.push(countByYear);
      runningTotal += installations.length;
      let overTimeByYear = {};
      overTimeByYear["year"] = year;
      overTimeByYear["count"] = runningTotal;
      overTimeData.push(overTimeByYear);
    }

    var byYearJson = {};
    byYearJson.title = "Dataverse Installations by Year";
    byYearJson.data = byYearData;
    byYearJson.divId = "chartByYear";
    addChart(byYearJson);

    var overTimeJson = {};
    overTimeJson.title = "Dataverse Installations Over Time";
    overTimeJson.data = overTimeData;
    overTimeJson.divId = "chartOverTime";
    addChart(overTimeJson);
  });
});

function addChart(chartJson) {
  var chartDiv = document.createElement("div");
  var barChart = document.createElement("table");
  var titleRow = document.createElement("tr");
  var titleData = document.createElement("td");
  titleData.setAttribute("colspan", chartJson.data.length + 1);
  titleData.setAttribute("class", "chartTitle");
  titleData.innerText = chartJson.title;
  titleRow.appendChild(titleData);
  barChart.appendChild(titleRow);
  chartDiv.appendChild(barChart);

  var barRow = document.createElement("tr");

  for (var i = 0; i < chartJson.data.length; i++) {
    barRow.setAttribute("class", "bars");
    var barData = document.createElement("td");
    var bar = document.createElement("div");
    bar.setAttribute("class", "barColor");
    bar.style.height = chartJson.data[i]["count"] / 4 + "em";
    barData.innerText = chartJson.data[i]["count"];
    barData.appendChild(bar);
    var yearSpan = document.createElement("span");
    yearSpan.className = "barDate";
    yearSpan.innerText = chartJson.data[i]["year"];
    barData.appendChild(yearSpan);
    barRow.appendChild(barData);
  }

  barChart.appendChild(barRow);
  chartDiv.appendChild(barChart);
  document.getElementById(chartJson.divId).innerHTML = chartDiv.outerHTML;
}
