var GoogleSpreadsheets = require('google-spreadsheets');
var fs = require('fs');
var buf = "";

var col = parseInt(process.argv[3]);
var row = parseInt(process.argv[2]);


CLIENT_ID = '1083549263547-2rp85g51in8kl864ch7nisoehepk2odu.apps.googleusercontent.com';
CLIENT_SECRET = 'c7APBFFW55IVgp5BAvMZYT7b';
REDIRECT_URL = 'techlab.tl';

// OPTIONAL: if you want to perform authenticated requests.
// You must install this dependency yourself if you need it.
var google = require('googleapis');

var oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URL);
ACCESS_TOKEN = 'ya29..xAICNFvy9E2ES48gE0hlJlMKJPzhk9WamcIq9t5wOCJ6NsIM8ZxKxdD_kJpgq6i9Jg';
REFRESH_TOKEN = '1/A43PCiEpucRYsRXxDp_-iqaK1Os3J1yEM16Z0xnTTDs';
// Assuming you already obtained an OAuth2 token that has access to the correct scopes somehow...
oauth2Client.setCredentials({
    access_token: ACCESS_TOKEN,
    refresh_token: REFRESH_TOKEN
});

GoogleSpreadsheets({
    key: '1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380',
    auth: oauth2Client
  }, function(err, spreadsheet) {
      spreadsheet.worksheets[0].cells({
          range: "R2C2:R205C3"
      }, function(err, result) {
      	buff = result.cells[row][col].value;
      });
  });

  fs.writeFile("/home/pi/Documents/Database/buffer", "Hey there!", function(err) {
      if(err) {
          return console.log(err);
      }
  });
