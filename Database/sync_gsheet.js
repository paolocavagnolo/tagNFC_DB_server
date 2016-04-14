var Spreadsheet = require('edit-google-spreadsheet');

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

    spreadsheet.add({ 3: { 3: "5" } });

    spreadsheet.send(function(err) {
      if(err) throw err;
    });

});
