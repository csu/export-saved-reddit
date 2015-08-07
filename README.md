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
    python export-saved.py

Without git, [download the source code from GitHub](https://github.com/csu/export-saved-reddit/archive/master.zip), extract the archive, and follow the steps above beginning from the second line.

## Usage
    export-saved.py [-h] [--user USER] [--password PASSWORD]
                       csv_output html_output

positional arguments:

    csv_output           path to csv file.
    html_output          path to html bookmark file.

optional arguments:

    -h, --help           show this help message and exit
    --user USER          Reddit username.
    --password PASSWORD  Reddit user password.
