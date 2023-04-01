// inspired by https://gist.github.com/richard-flosi/b6cdba782576447fcc9789f6cdfe2e31
class ByCountry extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: 'open' });
  }
  static get observedAttributes() {
    return ['loading', 'jsonData'];
  }
  get loading() {
    return JSON.parse(this.getAttribute('loading'));
  }
  set loading(v) {
    this.setAttribute('loading', JSON.stringify(v));
  }
  get jsonData() {
    return JSON.parse(this.getAttribute('jsonData'));
  }
  set jsonData(v) {
    this.setAttribute('jsonData', JSON.stringify(v));
  }
  async fetchJsonData(url) {
    this.loading = true;
    const response = await fetch(url);
    const json = await response.json();
    this.jsonData = json;
    this.loading = false;
  }
  async connectedCallback() {
    await this.fetchJsonData('data/data.json');
  }
  attributeChangedCallback(attrName, oldVal, newVal) {
    this.render();
  }
  render() {
    if (this.loading) {
      this.shadowRoot.innerHTML = `Loading...`;
    } else {
      var installations = this.jsonData.installations;
      var byCountryUnsorted = {};
      for (var i = 0; i < installations.length; i++) {
        var installation = installations[i];
        var country = installation.country;
        if (byCountryUnsorted[country] == undefined) {
          byCountryUnsorted[country] = [];
        }
        byCountryUnsorted[country].push(installation);
      }
      var byCountrySorted = Object.keys(byCountryUnsorted)
        .sort()
        .reduce((obj, key) => {
          obj[key] = byCountryUnsorted[key];
          return obj;
        }, {});
      // An array of objects with the name of the country and data about each installation in that country.
      var byCountryFinal = [];
      for (country in byCountrySorted) {
        var dataPerCountry = {};
        dataPerCountry.name = country;
        dataPerCountry.installations = [];
        for (i in byCountrySorted[country]) {
          var site = byCountrySorted[country][i];
          var bar = '<a href="http://' + site.hostname + '">' + site.name + '</a>';
          dataPerCountry.installations.push(bar);
        }
        byCountryFinal.push(dataPerCountry);
      }
      this.shadowRoot.innerHTML = `
<h3>${byCountryFinal.length} Countries</slot></h3>
<!-- TODO: Use css for table border -->
<table border=1>
  <tr>
    <th>Name</th>
    <th>#</th>
    <th>Installations</th>
  </tr>
  ${byCountryFinal
    .map(country => {
      return `
  <tr>
     <td>${country.name}</td>
     <td>${country.installations.length}</td>
     <!--TODO: Get rid of commas from javascript template literals: https://stackoverflow.com/questions/62690538/why-are-there-commas-in-my-output-when-i-use-map-in-a-template-literal -->
     <td>${country.installations}</td>
  </tr>
  `;
    })
    .join('')}
</table>
        `;
    }
  }
}
customElements.define('by-country', ByCountry);
