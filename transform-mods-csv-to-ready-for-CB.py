# transform-mods-csv-to-ready-for-CB.py
##
## This script, evolved from rootstalk-google-sheet-to-front-matter.py from my 
## https://github.com/Digital-Grinnell/hugo-front-matter-tools project, is designed to read all 
## exported MODS records from the `mods.csv` tab of  https://docs.google.com/spreadsheets/d/1ic4PxHDbuzDrmf4YtauhC4vEQJxt3QSH8bYfLBCM3Gc/edit#gid=935629805
## and transform that data into a new ready-for-CB datetime-named tab of the same Google Sheet, but using the column 
## heading/structure of the CollectionBuilder demo `Sheet1` tab.

# import glob
# import pathlib
# import sys
# from queue import Empty
# from typing import Dict

import os
import csv
import inspect
import tempfile
import gspread as gs
from datetime import datetime

# Populate the "transform" dict.  THIS IS CRITICAL!  
# This dict maps MODS.csv headings either to a CB CSV heading, or to a function.
transform = {
  "PID": "objectid",
  "WORKSPACE": None,
  "Import_Index": { "tbd": None },
  "PARENT": "parentid",
  "CMODEL": { "simple_map": "display_template" },
  "SEQUENCE": { "tbd": None },
  "OBJ": { "filename": "object_location" },
  "TRANSCRIPT": { "filename": "transcript" },
  "THUMBNAIL": { "filename": "image_thumb" },
  "Title": "title",
  "Alternative_Titles": { "tbd": None },
  "Personal_Names~Roles": { "name_with_attribute": "creator" },
  "Corporate_Names~Roles": { "tbd": None },
  "Abstract": "description",
  "Index_Date": "date",
  "Date_Issued": { "tbd": None },
  "Date_Captured": { "tbd": None },
  "Other_Date~Display_Label": { "tbd": None },
  "Publisher": { "tbd": None },
  "Place_Of_Publication": { "tbd": None },
  "Public_Notes~Types": { "tbd": None },
  "Notes~Display_Label": { "tbd": None },
  "Dates_as_Notes~Display_Label": { "tbd": None },
  "Citations": { "tbd": None },
  "Table_of_Contents": { "tbd": None },
  "LCSH_Subjects": { "tbd": None },
  "Subjects_Names~Types": { "tbd": None },
  "Subjects_Geographic": { "simple_list": "location" },
  "Subjects_Temporal": { "tbd": None },
  "Keywords": { "simple_list": "subject" },
  "Coordinate": { "tbd": None },
  "Related_Items~Types": { "tbd": None },
  "Type_of_Resource~AuthorityURI": { "name_with_attribute": "type" },
  "Genre~AuthorityURI": { "tbd": None },
  "Extent": { "tbd": None },
  "Form~AuthorityURI": { "tbd": None },
  "MIME_Type": "format",
  "Digital_Origin": { "tbd": None },
  "Classifications~Authorities": { "tbd": None },
  "Language_Names~Codes": "language",
  "Local_Identifier": "identifier",
  "Handle":	{ "tbd": None },
  "Physical_Location": { "tbd": None },
  "Shelf_Locator": { "tbd": None },
  "Access_Condition": "rightsstatement",
  "Import_Source": None,
  "Primary_Sort": None,
  "Hidden_Creator": { "tbd": None },
  "Pull_Quotes": { "tbd": None },
  "Private_Notes~Types": { "tbd": None }
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

# tbd: no transform defined at this time
def tbd( value, from_column, to ):
  func = inspect.currentframe().f_code.co_name
  if to is None:
    print("Transform function '{}' for column '{}' maps to None, skip it!".format(func, from_column))
    return False
  else:
    print("Function '{}' for column '{}' called with argument '{}' but I don't know what to do!".format(func, from_column, value))
  return value

# name_with_attribute: a single value with a single attribute
def name_with_attribute( value, from_column, to ):
  func = inspect.currentframe().f_code.co_name
  if to is None:
    print("Transform function '{}' for column '{}' maps to None, skip it!".format(func, from_column))
    return False
  else:
    print("Function '{}' for column '{}' called with argument '{}' but I don't know what to do!".format(func, from_column, value))
  return False

# filename: a filepath or URL to be translated as-is to a new column
def filename( value, from_column, to ):
  func = inspect.currentframe().f_code.co_name
  if to is None:
    print("Transform function '{}' for column '{}' maps to None, skip it!".format(func, from_column))
    return False
  else:
    print("Function '{}' for column '{}' called with argument '{}' but I don't know what to do!".format(func, from_column, value))
  return False

# simple_list: a simple list to translate into a single-value column
def simple_list( value, from_column, to ):
  func = inspect.currentframe().f_code.co_name
  if to is None:
    print("Transform function '{}' for column '{}' maps to None, skip it!".format(func, from_column))
    return False
  else:
    print("Function '{}' for column '{}' called with argument '{}' but I don't know what to do!".format(func, from_column, value))
  return False

# simple_map: a single value from controlled vocab to translate into a single-value column
def simple_map( value, from_column, to ):
  func = inspect.currentframe().f_code.co_name
  if to is None:
    print("Transform function '{}' for column '{}' maps to None, skip it!".format(func, from_column))
    return False
  else:
    print("Function '{}' for column '{}' called with argument '{}' but I don't know what to do!".format(func, from_column, value))
  return False

# Lifted from https://stackoverflow.com/a/54231563
#  csv_file - path to csv file to upload
#  sheet - a gspread.Spreadsheet object
#  cell - string giving starting cell, optionally including sheet/tab name
#    example: 'A1', 'MySheet!C3', etc.
def paste_csv(csv_file, sheet, cell):
  if '!' in cell:
    (tab_name, cell) = cell.split('!')
    wks = sheet.worksheet(tab_name)
  else:
    wks = sheet.sheet1
  (first_row, first_column) = gs.utils.a1_to_rowcol(cell)

  with open(csv_file, 'r') as f:
    csv_contents = f.read()
  body = {
    'requests': [{
      'pasteData': {
        "coordinate": {
          "sheetId": wks.id,
          "rowIndex": first_row-1,
          "columnIndex": first_column-1,
        },
        "data": csv_contents,
        "type": 'PASTE_NORMAL',
        "delimiter": ',',
      }
    }]
  }
  return sheet.batch_update(body)

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

      # Delete the temp file
      os.remove('temp.csv')

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
  for key in old_headings:
    if not key in transform:
      print("old_heading key '{}' does NOT exist in our 'transform' and needs to be accounted for!".format(key))
      exit( )

  # All clear, open a new temporary .csv file and begin transforming records
  # per https://community.esri.com/t5/python-questions/how-to-convert-a-google-spreadsheet-to-a-csv-file/td-p/452722
  
  with open('transformed.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)

    # Write the new_headings
    try:
      csvwriter.writerow(new_headings)
    except Exception as e:
      print(e)  

    # Loop on each record of data_records, and on each 'column' of the record, fetch the corresponding transform and apply it
    for record in data_records:
      transformed = dict.fromkeys(new_headings)
      for column in record:
        t = transform[column]
        if isinstance(t, str):              # transform is a string, save it as-is
          transformed[t] = record[column]
        elif isinstance(t, dict):           # dict, call the named function for processing
          key = list(t.keys())[0]
          func = globals()[key]
          r = func(record[column], column, t[key])
          if r:
            transformed[t[0]] = r
        elif t is None:                     # NO transform, skip this column 
          pass
        else:  
          print("transform[] for column '{}' is UNRECOGNIZED type '{}'".format(column, type(t)))

      # Write the transformed record
      try:
        csvwriter.writerow(transformed.values())
      except Exception as e:
        print(e)  
  
    # Write the temporary transformed .csv to a new tab in our Google Sheet
    # Make a datestamp to name the new worksheet
    new_tab = datetime.now().strftime("%Y-%b-%d-%I:%M%p")
  
    # Create the new/empty worksheet
    try:
      worksheet = sh.add_worksheet(title=new_tab, rows=1, cols=1)
    except Exception as e:
      print(e)  

    # Call our function to write the new Google Sheet worksheet
    try:
      paste_csv('transformed.csv', sh, new_tab + "!A1")
    except Exception as e:
      print(e)

    # Delete the temp file
    os.remove('transformed.csv')

  exit( )
