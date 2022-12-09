
# transform-mods-csv-to-ready-for-CB

This script, evolved from rootstalk-google-sheet-to-front-matter.py from my 
https://github.com/Digital-Grinnell/hugo-front-matter-tools project, is designed to read all 
exported MODS records from the `mods.csv` tab of  https://docs.google.com/spreadsheets/d/1ic4PxHDbuzDrmf4YtauhC4vEQJxt3QSH8bYfLBCM3Gc/edit#gid=935629805
and transform that data into a new `ready-for-CB` tab of the same Google Sheet, but using the column 
heading/structure of the CollectionBuilder demo `Sheet1` tab.

---

# Hugo Front Matter Tools

A collection of Python scripts desinged to help manage [Hugo](https://gohugo.io) `.md` content [front matter](https://gohugo.io/content-management/front-matter/).

---

## Python

See [Proper Python](https://blog.summittdweller.com/posts/2022/09/proper-python/) for applicable guidance when enabling Python parts of this workflow.  

### Quick Start

Since the project's Python infrastructure has already been created, but is not saved in our _GitHub_ repo, all you need to do to get started locally is this:

```bash
╭─mcfatem@MAC02FK0XXQ05Q ~/GitHub/hugo-front-matter-tools ‹main› 
╰─$ git pull
Already up to date.
╭─mcfatem@MAC02FK0XXQ05Q ~/GitHub/hugo-front-matter-tools ‹main› 
╰─$ python3 -m venv .venv
╭─mcfatem@MAC02FK0XXQ05Q ~/GitHub/hugo-front-matter-tools ‹main●› 
╰─$ source .venv/bin/activate
(.venv) ╭─mcfatem@MAC02FK0XXQ05Q ~/GitHub/hugo-front-matter-tools ‹main●› 
╰─$ pip3 install -r python-requirements.txt
```

Then...

```
(.venv) ╭─mcfatem@MAC02FK0XXQ05Q ~/GitHub/hugo-front-matter-tools ‹main●›
╰─$ python3 rootstalk-front-matter-to-google-sheet.py
```
---

## front-matter-to-csv.py (Deprecated)

This script is/was designed to read all of the .md files in a directory tree, and populate a single .csv file with the contents/status of all the frontmatter found in those Markown files.  Inspired by [convert.py](https://git.kucharczyk.xyz/lukas/frontmatter-to-csv/src/branch/main/frontmatter_to_csv/convert.py) from the [lukas/frontmatter-to-csv](https://git.kucharczyk.xyz/lukas/frontmatter-to-csv) repo.  

## rootstalk-front-matter-to-google-sheet.py

Having evolved from `front-matter-to-csv.py`, this script is designed to read all of the ROOTSTALK .md files in a directory tree and populate a specified .csv file (and dedicated Google Sheet) with the contents/status of all the frontmatter found in those Markdown files.

This script is specific to _Rootstalk_ because many of the constants and static elements (documented below) have become specific to our _Rootstalk_ structure.  However, the concept of harvesting and reporting `.md` file front matter remains unchanged.  This script could easily be adapted to work with other front matter structures.  

Use this link to open the [_Rootstalk Articles Front Matter_ Google Sheet](https://docs.google.com/spreadsheets/d/1cOYyS5gwU3HbTG8aVkaBwFPL1Z_7U25bJBCKCePFafI/). 

---

### Link Generation

On October 25, 2022, a feature was added to this script for generation of links to corresponding "development" site pages.  So, for instance, the row of `.csv` data that previously contained this:

```csv
volume-viii-issue-1,trissell.md,Food Deserts in t...,9,trissell,,05/10/2022 15:22:00,False,1,author,Mikayla Trissell,Trissel-1-volume-...
```

...now contains this:

```csv
volume-viii-issue-1,trissell.md,https://icy-tree-020380010.azurestaticapps.net/volume-viii-issue-1/trissell ,Food Deserts in t...,9,trissell,,05/10/2022 15:22:00,False,1,author,Mikayla Trissell,Trissel-1-volume-...
```

A link to the article `trissell`, for our example, now appears in the 3rd column of the `.csv` data.  Clicking that link from any view of the `.csv` file should open the "icy-tree" development version of the current article.  Note that this version of the website is actively generated from the `main` branch of the _Rootstalk_ project code.

---

## Google Sheets Integration

Found what looks like useful, and current, guidance in [How to Connect Python to Google Sheets](https://blog.coupler.io/python-to-google-sheets/).  Opened a new `google-sheet` feature branch of the code, and away we go...

Switching guidance to the more relevant [Python quickstart](https://developers.google.com/sheets/api/quickstart/python) document.

- Choose to enable the Google Sheets API in my `hugo-frontmatter-tools` project.
- Had to add at leat one "test" user to get past app authentication, so `digital@grinnell.edu` was authorized as a test user.
- Remaining process was as-advertised and generated a new `credentials.json` file as expected.
- Ran `quickstart.py` on my Mac Mini to authorize the app here.  A `token.json` file was subsequently generated in the working directory.

Next, with `credentials.json` in-hand I moved back to the guidance at `How to enable Python access to Google Sheets` in [How to Connect Python to Google Sheets](https://blog.coupler.io/python-to-google-sheets/).

- Created the new `sheets.py` script and changed the spreadsheet title to `Rootstalk-Articles-Frontmatter-Export` in line 10.

**And apparently my `credentials.json` doesn't have the right format?**  Probably because [How to Connect Python to Google Sheets](https://blog.coupler.io/python-to-google-sheets/) is written for a web application, but I need a desktop app?
    
## Reset!

So, [this 12 minute 45 second video](https://www.youtube.com/watch?v=bu5wXjz2KvU) appears to be a much better, more relevant and elegantly simple, explanation!  This approach will leverage the [gspread](https://docs.gspread.org/en/v5.6.2/) Python library, and it assumes that we already have a Google Sheet (I'm going to make one very soon!) and we simply "share" it with the "service account" that we're going to create with `Google Drive API` and `Google Sheet API` services enabled.  

### Making the Google Sheet

1) First, I open https://google.com logged in as `digital@grinnell.edu`, the account that will own our new Google Sheet.  I select the Google Apps menu and pick `Sheets` which opens [this page](https://docs.google.com/spreadsheets/u/0/) which is specific to the `digital@grinnell.edu` account.  
2) Here I created my new "blank" [Google Sheet](https://docs.google.com/spreadsheets/d/1cOYyS5gwU3HbTG8aVkaBwFPL1Z_7U25bJBCKCePFafI/edit#gid=0) and changed it's name to `Rootstalk Articles Frontmatter`. 
3) I changed the name of `Sheet1` to `25-Oct-2022` to match today's date.
4) Then I selected `File` and `Import` from the menu, then `Upload`, and browsed to select the latest `frontmatter-status.csv` file for import.
5) I imported the `.csv` file to the current sheet.

The all-important Google Sheet ID is: https://docs.google.com/spreadsheets/d/1cOYyS5gwU3HbTG8aVkaBwFPL1Z_7U25bJBCKCePFafI

### Integration with the Google Sheet

Following the [video](https://www.youtube.com/watch?v=bu5wXjz2KvU) I did this...

1) From my Google Developer dashboard I selected the `hugo-frontmatter-tools` project I had created earlier.
2) I made sure both `Google Drive API` and `Google Sheets API` are enabled for the project.
3) Next, from https://console.cloud.google.com/apis/dashboard?project=hugo-frontmatter-tools I clicked `Credentials` in the left menu.
4) I clicked `Manage Service Accounts` just above the right end of the `Service Accounts` tab.
5) I clicked `Create Service Account` near the top-center of the window. 
6) In `Service Account Details` I gave my SA a name of `hugo-frontmatter-tools` which generated a corresponding ID with an email address of `hugo-formatter-tools@hugo-frontmatter-tools.iam.gserviceaccount.com`.  <-- **This is important!**
7) Clicked `Create and Continue` and accepted all defaults until `Done`.
8) I opened our [Google Sheet](https://docs.google.com/spreadsheets/d/1cOYyS5gwU3HbTG8aVkaBwFPL1Z_7U25bJBCKCePFafI) and used the `Share` button in the upper-right corner to open the `Share "Rootstalk Articles Frontmatter"` sheet dialog.
9) In the dialog I pasted the all-important service account email address from above, clicked `Share` (as an `Editor`), and then `Done`.
10) Back in the [service account page](https://console.cloud.google.com/iam-admin/serviceaccounts?project=hugo-frontmatter-tools) I clicked the three dots on the right and chose `Manage Keys` as instructed in the video.
11) I clicked `Add Key`, `Create New Key` and selected `JSON` and `CREATE`.  Google generated a new key and uploaded it as `hugo-frontmatter-tools-a027c8a25d36.json` in my `~/Downloads` folder.

That completes the credentials acquisition process.  Per the video I then returned to the project window here in _VSCode_ and...

1) Activate and enable the `gspread` project to our virtual environment like so:
  ```
  source .venv/bin/activate
  pip3 install gspread
  pip3 freeze > python-requirements.txt
  ```
2) Move the JSON key file to the required location, like so:
  ```
  mkdir ~/.config/gspread
  mv ~/Downloads/hugo-frontmatter-tools-a027c8a25d36.json ~/.config/gspread/service_account.json
  ```

**_Note_**: *Those last commands above will need to be repeated on other platforms before Google Sheet integration can be achieved there!*  

#### google-sheet-test.py

Time for some testing so I created the `google-sheet-test.py` script by borrowing code from the video's `script.py` source.  I changed specifics as necessary in the `open` and `worksheet` function calls, and commented out anything that could damage our data, to yield this:

```python
import gspread

sa = gspread.service_account()
sh = sa.open("Rootstalk Articles Front Matter")

wks = sh.worksheet("26-Oct-2022-09:08PM")

print('Rows: ', wks.row_count)
print('Cols: ', wks.col_count)

print(wks.acell('A9').value)
print(wks.cell(3, 4).value)
print(wks.get('A7:E9'))

# print(wks.get_all_records())
# print(wks.get_all_values())

# wks.update('A3', 'Anthony')
# wks.update('D2:E3', [['Engineering', 'Tennis'], ['Business', 'Pottery']])
# wks.update('F2', '=UPPER(E2)', raw=False)

# wks.delete_rows(25)
```

Running that code as a test produced this:

```bash
(.venv) ╭─mark@Marks-Mac-Mini ~/GitHub/hugo-front-matter-tools ‹google-sheet*› 
╰─$ /Users/mark/GitHub/hugo-frontmatter-tools/.venv/bin/python /Users/mark/GitHub/hugo-front-matter-tools/google-sheet-test.py
Rows:  1000
Cols:  26
volume-viii-issue-1
The Streets of Da...
[['volume-viii-issue-1', 'obrien.md', 'https://icy-tree-020380010.azurestaticapps.net/volume-viii-issue-1/obrien', 'A Woman and the Land', '7'], ['volume-viii-issue-1', 'kessel.md', 'https://icy-tree-020380010.azurestaticapps.net/volume-viii-issue-1/kessel', 'Prairie Style: Wr...', '14'], ['volume-viii-issue-1', 'thompson.md', 'https://icy-tree-020380010.azurestaticapps.net/volume-viii-issue-1/thompson', 'Dark Skies or Lig...', '4']]
```

__*Huzzah!*__

## Google Sheet Feature is Complete

Development of Google Sheet integration within the script prompted me to rename the old script from `front-matter-to-csv.py` to `front-matter-to-google-sheet.py`, but this new script still generates a new `front-matter-status.csv` file each time it's run.

After the `.csv` is generated the script attempts to open our _Rootstalk Articles Front Matter_ [Google Sheet](https://docs.google.com/spreadsheets/d/1cOYyS5gwU3HbTG8aVkaBwFPL1Z_7U25bJBCKCePFafI/) where it creates a new worksheet/tab named with the current date/time.  The `.csv` file contents are then uploaded to the new worksheet using this block of code:

```python
  try:
    paste_csv(csv_filename, sh, sheet_name + "!A1")
  except Exception as e:
    print(e)  
```

When it works we get a new worksheet/tab full of current front matter data in our all-important Google Sheet, https://docs.google.com/spreadsheets/d/1cOYyS5gwU3HbTG8aVkaBwFPL1Z_7U25bJBCKCePFafI/. 

## Documentation

Yes, there is more!  Check out [Google-Sheet-Front-Matter.mp4](https://rootstalk.blob.core.windows.net/documentation/Google-Sheet-Front-Matter.mp4) sometime when you have 15 minutes to kill.  :smile:

---

## Static Elements

Static elements of the script currently include the following.

### branches

List of the three code branches for which links are generated in the Google Sheet.

```python
branches = [ "develop", "main", "production" ]
```

### Expected Fields

```python
fields = {
  "md-path": "Content Path",
  "md-file": "Filename",
  "develop-link": "develop Link",
  "main-link": "main Link",
  "production-link": "Production Link",
  "title": "title",
  "last_modified_at": "last_modified_at",
  "to-do": "to-do List",
  "articleIndex": "articleIndex",
  "description": "description",
  "azure_dir": "azure_dir",
  "obsolete": "Obsolete Front Matter",
  "contributors": "contributors",
  "role": "contributor.role",
  "name": "contributor.name",
  "headshot": "contributor.headshot",
  "caption": "contributor.caption",
  "bio": "contributor.bio",
  "articletype": "articletype",
  "header_image": "header_image",
  "filename": "header_image.filename",
  "alt_text": "header_image.alt_text",
  "tags": "tags",
  "byline": "byline",
  "byline2": "byline2",
  "subtitle": "subtitle",
  "no_leaf_bug": "no_leaf_bug",
  "index": "index",
  "date": "date",
  "draft": "draft"
}
```

### Obsolete Fields

The following fields are considered "obsolete" and deprecated.  Articles that still posses these fields should be upgraded to use corresponding `fields` as soon as possible.

```python
obsolete = ["sidebar", "pid", "issueIndex", "azure_headerimage", "author", "azure_headshot", "authorbio", "headerimage"]
```

### Contributor `dict` Fields

```python
contributor_fields = ["role", "name", "headshot", "caption", "bio"]
```

### Header Image `dict` Fields

```python
header_image_fields = ["filename", "alt_text"]
```

### Input `glob` File Spec

```python
 filepath = str(pathlib.Path.home()) + "/GitHub/rootstalk/content/**/volume*/*.md"
```

### CSV Output Filename

```python
  csv_filename = "front-matter-status.csv"
 ```

### Link Generation Base URL

The links used here are automatically built by the two principal braches of the [Rootstalk project repo](https://github.com/Digital-Grinnell/rootstalk), and a third for production at https://rootstalk.grinnell.edu.

```python
def build_link(k, path):
  base_urls = { "develop":"https://thankful-flower-0a2308810.1.azurestaticapps.net/", "main":"https://icy-tree-020380010.azurestaticapps.net/", "production":"https://rootstalk.grinnell.edu/" }
```
