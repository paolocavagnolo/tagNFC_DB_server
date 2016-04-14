var GoogleSpreadsheet = require("google-spreadsheet");
var doc = new GoogleSpreadsheet('1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380');


var col = process.argv[4];
var row = process.argv[3];

var data = {};
data[row] = {};
data[row][col] = process.argv[2];

async.series({

  function setAuth(step) {
    // see notes below for authentication instructions!
    var creds = require('/home/pi/techlab-tag-nfc-01c55db202b2.json');
    // OR, if you cannot save the file locally (like on heroku)
  }
  doc.useServiceAccountAuth(creds, step);

});
