# Discourse Map
Display all Discourse users' location on Zeemaps.
This script allows you to get all users on a Discourse site and update
a Google Spreadsheet with the users' `location`.

By default only active users will be displayed, but this can be changed in `config.py`

## Installation
There are quite a few steps to install this script.

1. Download this python script, either with git or downloading a zip-file.
1. Rename `config.example.py` to `config.py` in `discoursemap`
    1. Open `config.py`
    1. Update `API_USERNAME` to your Discourse username.
    1. **If** you want to show all users (included suspended) change
    `SHOW_SUSPENDED` to `True`.
    1. We will update the rest of the config in other sections.
1. Get Discourse user API key.
    1. For this you have to message an admin (if you aren't one yourself).
    The admin can generate an user API key here:
    `admin --> Users --> click on the user --> scroll to Permissions section, API Key, press Generate`.
    1. Update `API_KEY` to the Discourse API key you got.
1. Create a new Google Spreadsheet.
    1. Update `SHEET_ID` in `config.py` to your sheet id. You can find
    the sheet's id in the url, it's the part between `spreadsheets/d/` and `/edit#gid=99999`.
    1. **If** you changed the sheet name, be sure to update the `SHEET_NAME` as well.
1. Create Google Spreadsheet API authorization. This is the most advanced part.
    1. Use [this wizard](https://console.developers.google.com/start/api?id=sheets.googleapis.com).
    1. Choose `Create a project`.
    1. Click `Go to credentials`.
    1. Click `Cancel` at the bottom.
    1. Click `Create credentials` and choose `OAuth client ID`.
    1. Click `Configure consent screen`
    1. Fill in `Product name shown to users` with `Discourse map` or something similar and click `Save`.
    1. Choose `Other`, name it `Discourse map` or similar and click `Create`.
    1. Click `OK`.
    1. Download the `client_secret.json` by clicking on the download icon furthest to the right.
    1. Save the `client_secret.json` file (with that exact name) in the same directory as `config.py`
1. Run the script by being in the `discourse-map` directory, run it with this command: `python -m discoursemap`
    1. You will now see a link to authorize this script to access your Google Spreadsheets.
    Copy the link to your browser and authorize this script. The next time you won't get this message if you followed
    the correct steps.
1. Done :)