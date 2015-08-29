# Installation

It requires `lxml` and `unicodecsv`, both can be installed with `pip`:

    pip install lxml
    pip install unicodecsv

On Ubuntu, you may also need to install additional packages with the following command:

    sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev

# Usage

Just run `ucscx.py` and redirect the output to a file:
    
    python ucscx.py > courses.csv

Then import the csv file to the application of your choice, e.g. Google Sheets, Microsoft Excel, Sqlite, etc.

Tested on OS X 10.11 Beta (15A262e) with Python 2.7.8.
