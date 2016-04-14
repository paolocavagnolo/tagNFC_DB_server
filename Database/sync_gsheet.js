var Spreadsheet = require('edit-google-spreadsheet');

row = 3;
col = 4;

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

    spreadsheet.add({ global.row: { global.col: process.argv[2] } });

    spreadsheet.send(function(err) {
      if(err) throw err;
    });

});
