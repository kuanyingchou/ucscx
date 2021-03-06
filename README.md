# Installation

It requires `lxml` and `unicodecsv`, both can be installed with `pip`:

    pip install lxml
    pip install unicodecsv

On Ubuntu, you may also need to install additional packages with the following command:

    sudo apt-get install libxml2-dev libxslt1-dev python-dev zlib1g-dev

# Usage

Just run `ucscx.py` and redirect the output to a file:
    
    python ucscx.py > courses.tsv

Then import the tsv file to the application of your choice, e.g. Google Sheets, Microsoft Excel, Sqlite, or shell commands.

For example, to get the ids and names of all the offerings in Bash, you can run:

    cut -d$'\t' -f1,2 courses.tsv

To get all the Java courses, run:

    cut -d$'\t' -f1,2 courses.tsv | grep -i java

Tested on OS X 10.11 Beta (15A262e) with Python 2.7.8.
