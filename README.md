# Export Saved
Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome.

## Dependencies
Requires:

* praw

## Usage
0. Run `pip install praw` if praw is not already installed.
1. Copy or rename `AccountDetails.py.example` to `AccountDetails.py` and add your Reddit credentials.
2. Run `python export-saved.py` in the directory or first `chmod +x` the script and then use `./export-saved.py`.
3. Take the exported HTML file (named `chrome-bookmarks.html`) and import it into your bookmarks through the Google Chrome bookmarks manager.