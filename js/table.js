if ('content' in document.createElement('template')) {
  // Instantiate the table with the existing HTML tbody
  // and the row with the template
  var template = document.querySelector('#installation-row');
  // Clone the new row and insert it into the table
  var tbody = document.querySelector('tbody');
  url = '../data/data.json';
  fetch(url).then(function(response) {
    response.text().then(function(text) {
      obj = JSON.parse(text);
      installations = obj.installations;
      for (var i = 0; i < installations.length; ++i) {
        name = installations[i].name;
        hostname = installations[i].hostname;
        country = installations[i].country;
        description = installations[i].description;
        // Clone the new row and insert it into the table
        var clone = document.importNode(template.content, true);
        td = clone.querySelectorAll('td');
        td[0].innerHTML =
          '<a target="_blank" rel="noopener noreferrer" href="http://' +
          hostname +
          '">' +
          name +
          '</a>';
        td[1].textContent = country;
        td[2].textContent = description;
        tbody.appendChild(clone);
      }
    });
  });
} else {
  // Find another way to add the rows to the table because
  // the HTML template element is not supported.
}
