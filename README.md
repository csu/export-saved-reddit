# Export Saved
Exports saved Reddit posts into a HTML file that is ready to be imported into Google Chrome. Sorts items into folders by subreddit.

## Requirements
* [Python 2.X](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (recommended)

## Installation
First, make sure you have [Python 2.X](https://www.python.org/downloads/), [pip](https://pip.pypa.io/en/stable/installing/), and [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) installed on your machine.

Run the following in your command prompt to install:

    git clone https://github.com/csu/export-saved-reddit.git
    cd export-saved-reddit
    pip install -r requirements.txt

To install without git, [download the source code from GitHub](https://github.com/csu/export-saved-reddit/archive/master.zip), extract the archive, and follow the steps above beginning from the second line.

## Usage
1. In the `export-saved-reddit` folder, rename the `AccountDetails.py.example` file to `AccountDetails.py`.
2. Open the `AccountDetails.py` in a text editor and enter your Reddit username and password within the corresponding quotation marks. Save and close the file.
3. Back in your shell, run `python export-saved.py` in the `export-saved-reddit` folder. This will run the export, which will create `chrome-bookmarks.html` and `export-saved.csv` files containing your data in the same folder.

### Additional Options

    usage: export-saved.py [-h] [-v] [-u]

    Exports saved Reddit posts into a HTML filethat is ready to be imported into
    Google Chrome

    optional arguments:
      -h, --help     show this help message and exit
      -v, --verbose  increase output verbosity
      -u, --upvoted  get upvoted posts instead of saved posts

## Help
If you have any questions or comments, please [open an issue on GitHub](https://github.com/csu/export-saved-reddit/issues) or [contact me](https://christopher.su/about/).