# td-scraper
Get account data from TD EasyWeb to `$anywhere`.

## Background
After moving to university, I started needing to track my expenses more carefully (for tax purposes). Unfortunately, the web portal my bank provides (TD EasyWeb) does not have the ability to edit transaction data (as far as I know). Therefore, it made sense to track this information in a spreadsheet! After a while, updating the spreadsheet got quite tedious, so I wanted a better way to get the data from TD's web portal into my spreadsheet. Since they don't provide an API, this project was born.

## Usage
1. Ensure you have `docker` installed.
1. Clone the repository locally.
1. Create a file `account_details.json` in the root directory, with this file format:
   ```json
    {
        "username": "<your_username>",
        "password": "<your_password"
    }
   ```
   Note that the last line is not required if you don't plan on uploading the data to Google Sheets.

1. Create a file `account_types.json` in the root directory, with this file format:
   ```json
    {
        "<account 1 name in EasyWeb>": "<account 1 shortname>",
        "<account 2 name in EasyWeb>": "<account 2 shortname>",
    }
   ```
1. Everything should just work now! Run `make` first, and assuming this succeeds, run `make test` to pull your data.
