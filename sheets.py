import pickle
import os.path
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

import scraper

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

POSITION_RANGE_NAME = "Analytics Computation!A13:C13"

def _sheets_api_log_in():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds)

    return service.spreadsheets()

def main():
    sheets = _sheets_api_log_in()

    config = open(".config", "r")
    contents = config.read().splitlines()
    spreadsheet_id = contents[2]
    config.close()

    result = sheets.values().get(
        spreadsheetId=spreadsheet_id,
        range=POSITION_RANGE_NAME,
    ).execute()
    values = result.get("values", [])

    if not values or not len(values) or len(values[0]) != 3:
        print("Failed to get read position.")
        return

    row = values[0]
    first_free_row = int(row[0])
    last_group_date = pd.to_datetime(row[1], format="%d/%m/%Y")
    first_row_of_last_group = int(row[2])

    df = scraper.get_scraped_data()[0]
    overlap = len(df[df["Date"] == last_group_date]) > 0
    base_index = first_row_of_last_group if overlap else first_free_row
    df.set_index("Date", inplace=True)
    df = df.truncate(last_group_date, copy=False)
    if overlap:
        trunc = df.index.drop_duplicates().values[0]
        df = df.truncate(trunc, copy=False)

    df["Account Total"] = ["=SUMIF(D$4:D{index}, concat(\"=\",D{index}),C$4:C{index})".format(index=(index + base_index)) for index in range(0, len(df.values))]
    df["Type Total"] = ["=SUMIF(E$4:E{index}, concat(\"=\",E{index}),$C$4:$C{index})".format(index=(index + base_index)) for index in range(0, len(df.values))]

    values = df.values.tolist()
    index_values = df.index.tolist()
    values = [[index_values[i].strftime("%d/%m/%Y")] + values[i] for i in range(0, len(values))]

    write_range = "Data!A{}:G{}".format(base_index, base_index + len(df.index))
    result = sheets.values().update(
        spreadsheetId=spreadsheet_id,
        range=write_range,
        valueInputOption="USER_ENTERED",
        body={"values": values},
    ).execute()
    print("{0} cells updated.".format(result.get("updatedCells", -1)))
    input("Please press enter to continue.")

if __name__ == "__main__":
    main()
