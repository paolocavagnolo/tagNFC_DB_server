var GoogleSpreadsheets = require('google-spreadsheets');

CLIENT_ID = 1083549263547-2rp85g51in8kl864ch7nisoehepk2odu.apps.googleusercontent.com;
CLIENT_SECRET = c7APBFFW55IVgp5BAvMZYT7b;
REDIRECT_URL = techlab.tl;

// OPTIONAL: if you want to perform authenticated requests.
// You must install this dependency yourself if you need it.
var google = require('googleapis');

var oauth2Client = new google.auth.OAuth2(CLIENT_ID, CLIENT_SECRET, REDIRECT_URL);
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
        range: 'R1C1:R5C5'
    }, function(err, cells) {
        // Cells will contain a 2 dimensional array with all cell data in the
        // range requested.
    });
});
