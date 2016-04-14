var Spreadsheet = require('edit-google-spreadsheet');

var col = process.argv[4];
var row = process.argv[3];


var data = {};
data[row] = {};
data[row][col] = process.argv[2];

Spreadsheet.load({
    debug: true,
    spreadsheetId: '1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380',
    worksheetId: "od6",

    oauth : {
        email: 'techlab@techlab-tag-nfc.iam.gserviceaccount.com',
        keyFile: '/home/pi/techlab-key.pem'
    }

}, function sheetReady(err, spreadsheet) {

    if (err) throw err;

    // spreadsheet.add(data);
    //
    // spreadsheet.send(function(err) {
    //   if(err) throw err;
    // });
    spreadsheet.receive(function(err, rows, info) {
      if(err) throw err;
      console.log("Found rows:", rows);
      // Found rows: { '3': { '5': 'hello!' } }
    });


});
