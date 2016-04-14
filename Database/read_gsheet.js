var GoogleSpreadsheets = require('google-spreadsheets');
var fs = require('fs');
var buff = "";

var col = parseInt(process.argv[3]);
var row = parseInt(process.argv[2]);


CLIENT_ID = '1083549263547-2rp85g51in8kl864ch7nisoehepk2odu.apps.googleusercontent.com';
CLIENT_SECRET = 'c7APBFFW55IVgp5BAvMZYT7b';
REDIRECT_URL = 'techlab.tl';

// OPTIONAL: if you want to perform authenticated requests.
// You must install this dependency yourself if you need it.
var google = require('googleapis');

GoogleSpreadsheets({
    key: '1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380',
  }, function(err, spreadsheet) {
      spreadsheet.worksheets[0].cells({
          range: "R2C2:R205C3"
      }, function(err, result) {
      	buff = result.cells[row][col].value;
      });
  });

  fs.writeFile("/home/pi/Documents/Database/buffer", buff, function(err) {
      if(err) {
          return console.log(err);
      }
  });
