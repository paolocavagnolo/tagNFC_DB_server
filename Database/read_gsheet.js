var GoogleSpreadsheets = require('google-spreadsheets');
var fs = require('fs');
var buff = "";

var col = parseInt(process.argv[3]);
var row = parseInt(process.argv[2]);


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
