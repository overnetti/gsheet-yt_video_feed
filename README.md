# Google Sheet Presentation Tracker Automator and Youtube updater

## Introduction
#### `video-feed-importer.py`
The python script `video-feed-importer.py` creates a Google Sheet for the USENIX Association with columns for the nodes, titles, authors, and abstracts from the program or technical sessions page. This creates a Presentation Tracker for the non-profit that allows team members to track presentations through the conference life cycle and ultimately prepare the presentations for posting to Youtube after the conference has concluded.

#### `yt_updater.py` (WIP)
The python script `yt_updater.py` utilizes the Gsheet created from `video-feed-importer.py` to update the titles and descriptions of presentation videos in a Youtube playlist. The script will update videos in the order that the `video-feed-importer.py` script scraped the program page (top to bottom) so it is essential for the videos to be arranged in this order in the playlist. The script will also store the links of each video and push a new "video" column to the Gsheet with those links for the Drupal feed import.

The USENIX Association is an advanced computing systems nonprofit organization, known for organizing conferences and publishing research. The organization hosts about 1 conference each moonth throughout the year, and team members are tasked with aggregating data manually from the conference technical sessions or program pages in order to set up a Presentation Tracker Gsheet. Presentations are tracked by teamm members to ensure that materials like consent forms and slides are received before the conference. After a conference concludes, this Gsheet serves as a video tracker to keep track of presentation recordings and the editing status for each. The task of setting up this spreadsheet is assigned to a team member for 1-2 weeks and this script removes the bulk of manual labor. The second half of this script updates video titles and descriptions on Youtube and retrieves the links for each video in preparation for updating the Drupal webpage with Youtube presentation links. In total, this project saves a team member ~300 hours annually.

## Need to Know

#### `video-feed-importer.py`
- Expected execution time: 1-10min, depending on size of program/technical sessions page due to a 3 second timer on writing to Gsheets to avoid receiving an error.
- User will need to create a spreadsheet beforehand in Drive and add the spreadsheet name to the `spreadsheet` variable (line 56)
- User will need to update the `yt_descs` variable to ensure the correct event is prefixed. (line 43)
- User will need to update the links in the variables `title`, `abstracts`, `nodes`, and `authors` to point to the conference of interest. (line 38-41)
- In its current state, the user will need to run the script on the terminal.

#### `yt_updater.py` (WIP)
- Expected execution time: 1-10min, depending on size of program/technical sessions.
- User will need to upload presentation videos manually.
- Videos MUST be arranged in program order, mirroring the Gsheet that the `video-feed-importer.py` script generated. 
- Youtube functionalities will need to be added to the users Google API.
- User will need to add the playlistID of the playlist to the `playlistID=` field in the `playlist_response` variable on line 38.

## Guidelines

#### Execution

`video-feed-importer.py`
1. Create a spreadsheet in your Drive for the data. 
2. Add the spreadsheet name to the `spreadsheet` variable (line 56).
3. Update the `yt_descs` variable to ensure the correct event is prefixed (line 43).
4. Update the links in the variables `title`, `abstracts`, `nodes`, and `authors` to point to the conference of interest (line 38-41).
5. In the terminal, navigate to the location of the `video-feed-importer.py` script.
6. Run the script using `python video-feed-importer.py` and the Gsheet will begin populating.

`yt_desc.py`
1. Upload the videos to Youtube manually and arrange them in a Playlist in the same order the `video-feed-importer.py` generated them in the Gsheet.
2. Navigate to the playlist and retrieve the playlistID from the link (Example: https://www.youtube.com/playlist?list=<playlist ID>)
3. Add the playlistID to the `playlistID=` field in the `playlist_response` variable on line 38.
4. In the terminal, navigate to the location of the `yt_desc.py` script.
5. Run the script using `python yt_desc.py` and the Youtube videos will begin renaming. (WIP) 


#### Dependencies for execution

#### `video-feed-importer.py`
1. Python 3.8 or higher
2. `pip install re`
3. `pip install time`
4. `pip install bs4`
5. `pip install urliib.request`
6. `pip install gspread`
7. Refer to docs.gspread.org for documentation on Google API set up. (https://docs.gspread.org/en/latest/)

#### `yt_updater.py`
1. Python 3.8 or higher
2. `pip install httplib2`
3. `pip install os`
4. Refer to Google API documentation for set up: https://developers.google.com/youtube/v3

## Future Improvements
1. The `video-feed-importer.py` should take the program page or technical sessions link as an input.
2. Project should have an .exe file for a smooth user experience.
