# Export Saved
Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome. Sorts items into folders by subreddit.

## Requirements
* Python 2.X
* pip
* git (recommended)

## Installation
With git:

    git clone https://github.com/csu/export-saved-reddit.git
    cd export-saved-reddit
    pip install -r requirements.txt

Without git, [download the source code from GitHub](https://github.com/csu/export-saved-reddit/archive/master.zip), extract the archive, and follow the steps above beginning from the second line.

## Usage

Rename 'AccountDetails.py.example' into 'AccountDetails.py' and put your reddit username and password.

After that run 'export-saved.py'.

It will create 'chrome-bookmarks.html' html bookmark and 'export-saved.csv' csv.