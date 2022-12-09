# transform-mods-csv-to-ready-for-CB.py
##
## This script, evolved from rootstalk-google-sheet-to-front-matter.py from my 
## https://github.com/Digital-Grinnell/hugo-front-matter-tools project, is designed to read all 
## exported MODS records from the `mods.csv` tab of  https://docs.google.com/spreadsheets/d/1ic4PxHDbuzDrmf4YtauhC4vEQJxt3QSH8bYfLBCM3Gc/edit#gid=935629805
## and transform that data into a new `ready-for-CB` tab of the same Google Sheet, but using the column 
## heading/structure of the CollectionBuilder demo `Sheet1` tab.

# import os
# import glob
# import pathlib
# import sys
# import tempfile
# from queue import Empty
# from typing import Dict
# from datetime import datetime

import csv
import gspread as gs

# Populate the "transform" dict.  THIS IS CRITICAL!  
# This dict maps MODS.csv headings either to a CB CSV heading, or to a function.
transform = {
  "PID": "objectid",
  "WORKSPACE": None,
  "Import_Index": { "exception": None },
  "PARENT": "parentid",
  "CMODEL": { "simple_map": "display_template" },
  "SEQUENCE": { "exception": None },
  "OBJ": { "filename": "object_location" },
  "TRANSCRIPT": { "filename": "transcript" },
  "THUMBNAIL": { "filename": "image_thumb" },
  "Title": "title",
  "Alternative_Titles": { "exception": None },
  "Personal_Names~Roles": { "name_with_attribute": "creator" },
  "Corporate_Names~Roles": { "exception": None },
  "Abstract": "description",
  "Index_Date": "date",
  "Date_Issued": { "exception": None },
  "Date_Captured": { "exception": None },
  "Other_Date~Display_Label": { "exception": None },
  "Publisher": { "exception": None },
  "Place_Of_Publication": { "exception": None },
  "Public_Notes~Types": { "exception": None },
  "Notes~Display_Label": { "exception": None },
  "Dates_as_Notes~Display_Label": { "exception": None },
  "Citations": { "exception": None },
  "Table_of_Contents": { "exception": None },
  "LCSH_Subjects": { "exception": None },
  "Subjects_Names~Types": { "exception": None },
  "Subjects_Geographic": { "simple_list": "location" },
  "Subjects_Temporal": { "exception": None },
  "Keywords": { "simple_list": "subject" },
  "Coordinate": { "exception": None },
  "Related_Items~Types": { "exception": None },
  "Type_of_Resource~AuthorityURI": { "name_with_attribute": "type" },
  "Genre~AuthorityURI": { "exception": None },
  "Extent": { "exception": None },
  "Form~AuthorityURI": { "exception": None },
  "MIME_Type": "format",
  "Digital_Origin": { "exception": None },
  "Classifications~Authorities": { "exception": None },
  "Language_Names~Codes": { "simple": "language" },
  "Local_Identifier": "identifier",
  "Handle":	{ "exception": None },
  "Physical_Location": { "exception": None },
  "Shelf_Locator": { "exception": None },
  "Access_Condition": "rightsstatement",
  "Import_Source": None,
  "Primary_Sort": None,
  "Hidden_Creator": { "exception": None },
  "Pull_Quotes": { "exception": None },
  "Private_Notes~Types": { "exception": None }
}

required_by_CB = [
  "objectid",
  "title",
  "display_template",
  "object_location",
  "image_small",
  "image_thumb",
  "format"
]

# exception: no transform defined at this time
def exception( value, from_column, to_column ):
  return True

# name_with_attribute: a single value with a single attribute
def name_with_attribute( value, from_column, to_column ):
  return True

# filename: a filepath or URL to be translated as-is to a new column
def filename( value, from_column, to_column ):
  return True  

# simple_list: a simple list to translate into a single-value column
def simple_list( value, from_column, to_column ):
  return True

# simple_map: a single value from controlled vocab to translate into a single-value column
def simple_map( value, from_column, to_column ):
  return True


######################################################################

# Main...
if __name__ == '__main__':

  sheetName = "CB-CSV_DG-01"   # Eventually this needs to be an input parameter, not hardcoded

  # Open the Google service account and sheet.  
  # See https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account Step 8 for details!
  try:
    sa = gs.service_account()
  except Exception as e:
    print(e)

  try:  
    sh = sa.open(sheetName) 
  except Exception as e:
    print(e)  

  # Read all worksheets from the Google Sheet, and find the sheets named "mods.csv" and "Sheet1"
  sheets = sh.worksheets()
  for ws in sheets:
    title = ws.title

    # Found the "mods.csv" sheet
    if (title == "mods.csv"):
      # old_headings is row_values(1), save it 
      old_headings = ws.row_values(1)

      # Generate a temporary .csv of the worksheet 
      # per https://community.esri.com/t5/python-questions/how-to-convert-a-google-spreadsheet-to-a-csv-file/td-p/452722
      with open('temp.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerows(ws.get_all_values())

      # Read the temporary .csv into a dict and save in data_records[]
      data_records = []
      with open('temp.csv', 'r') as data:
        for record in csv.DictReader(data):
          data_records.append(record)

    # Found the "Sheet1" sheet, grab just the column headings from row 1
    if (title == "Sheet1"):
      new_headings = ws.row_values(1)

  # End of the "ws in sheets" loop, check that we have old_headings, new_headings, and data_records
  if not old_headings:
    print("Check the {} sheet for valid 'mods.csv' headings, none found?".format(sheetName))
    exit( )

  if not data_records:
    print("Check the {} sheet for valid 'mods.csv' data, no data_records found?".format(sheetName))
    exit( )

  if not new_headings:
    print("Check the {} sheet for valid 'Sheet1' headings, none found?".format(sheetName))
    exit( )

  # Check that all of the old_headings are accounted for as keys in our "transform".  Report any that are not!
  # LATER

  # All clear, open a new temporary .csv file and begin transforming records
  # per https://community.esri.com/t5/python-questions/how-to-convert-a-google-spreadsheet-to-a-csv-file/td-p/452722
  with open('transformed.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the new_headings
    try:
      csvwriter.writerow(new_headings)
    except Exception as e:
      print(e)  

  exit( )
