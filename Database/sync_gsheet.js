var Spreadsheet = require('edit-google-spreadsheet');

var data = {};
data[parseInt(process.argv[3])] = {};
data[parseInt(process.argv[4])] = process.argv[2];

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

    spreadsheet.add(data);

    spreadsheet.send(function(err) {
      if(err) throw err;
    });

});
