"use strict";

if (window.location.pathname == "/home") {
  document.querySelector("body > form").addEventListener("submit", ()=>{
    event.preventDefault();

    let formData = new FormData(event.target);

    fetch('http://localhost/home', {
      credentials: 'same-origin',
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({
          for: 'URLcheck',
          URL: formData.get("URL")
        }),
    })
    .then(response => response.json()).then(data => {
      if (!!!data["HTTPErrorResponse"] && data["PythonResponse"] == "OK") {
        document.querySelector("body > section[for=result]").innerHTML = `
          <h1>Result</h1>
          <table>
            <tr>
              <th>STATUS</th>
              <th>STATUS DESCRIPTION</th>
              <th>URL</th>
              <th>RESPONSE TIME</th>
            </tr>
            <tr>
              <td>${data["data"]["status"]}</td>
              <td>${data["data"]["statusDescription"]}</td>
              <td>${data["data"]["url"]}</td>
              <td>${data["data"]["responseTime"]}</td>
            </tr>
          </table>
        `;
      }
      if (!!data["HTTPErrorResponse"]){
        document.querySelector("body > section[for=result]").innerHTML = `<h1>${data["HTTPErrorResponse"]}</h1>`;
      }
    }).catch((error) => {
      console.error('Error:', error);
    });
  });
}
