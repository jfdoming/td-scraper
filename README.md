# td-scraper
Scrape account data from TD EasyWeb.

## Background
After moving to university, I started needing to track my expenses more carefully (for tax purposes). Unfortunately, the web portal my bank provides (TD EasyWeb) does not have the ability to edit transaction data (as far as I know). Therefore, it made sense to track this information in a spreadsheet! After a while, updating the spreadsheet got quite tedious, so I wanted a better way to get the data from TD's web portal into my spreadsheet. Since they don't provide an API, this project was born.

## Usage
1. Clone the repository locally.
2. Create a file ".config" in the root directory, with this file format:
   ```
   <line 1=TD username>
   <line 2=TD password>
   <line 3=Google Sheets spreadsheet ID>
   ```
   Note that the last line is not required if you don't plan on uploading the data to Google Sheets.

3. Create a file "account_details.py" in the root directory, containing the following Python dictionary:
   ```python
   ACCOUNT_TYPES = {
       "<account 1 name in EasyWeb>": "<account 1 name in spreadsheet>",
       "<account 2 name in EasyWeb>": "<account 2 name in spreadsheet>",
   }
   ```
4. Create a directory "data/" in the root directory.
5. Everything should just work now! Run `scraper.py` first, and assuming this succeeds, run `sheets.py` to upload the data to Google Sheets.
