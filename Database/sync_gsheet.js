var Spreadsheet = require('edit-google-spreadsheet');

Spreadsheet.load({
    debug: true,
    spreadsheetId: '1gBOByKgaDgbneWOBalxZ5jihJVV1iUFKuytqGVUG380',
    worksheetName: 'Foglio1',

    oauth : {
        email: 'techlab@techlab-tag-nfc.iam.gserviceaccount.com',
        keyFile: '/home/pi/techlab-key.pem'
    }

}, function sheetReady(err, spreadsheet) {

    if (err) throw err;

    spreadsheet.add({ 3: { 5: "hello!" } });

    spreadsheet.send(function(err) {
      if(err) throw err;
      console.log("Updated Cell at row 3, column 5 to 'hello!'");
    });

});
