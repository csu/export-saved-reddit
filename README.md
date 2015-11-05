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

# Usage
1. In the `export-saved-reddit` folder (created by the `git clone`), rename the `AccountDetails.py.example` file to `AccountDetails.py`.
2. Open the `AccountDetails.py` in a plain text editor and enter your Reddit username and password within the corresponding quotation marks. Save and close the file.
3. Back in your shell, run `python export-saved.py` in the `export-saved-reddit` folder. This will run the export, which will create `chrome-bookmarks.html` and `export-saved.csv` files containing your data in the same folder.