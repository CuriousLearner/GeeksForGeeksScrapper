# GeeksForGeeksScrapper
Scrapes [GeeksForGeeks](http://www.geeksforgeeks.org) and creates html & PDF for chosen category along with syntax highlighting for the code.

## Installation
To use the scrapper, install the following:

`$ sudo apt-get install wkhtmltopdf`

Then create venv

`$ virtualenv /path/to/g4g-env`

Switch to venv

`$ source /path/to/g4g-env/bin/activate`

Now install BeautifulSoup as:

`$ pip install beautifulsoup4`

or via package manager as:

`$ sudo apt-get install python-bs4`

## Run the G4G_Scrapper

$ python g4g.py

Choose the category you want to scrape from the menu and wait for the magic to happen :)

You can find the output as `G4G_<category_name>.html` and `G4G_<category_name>.pdf` in the same directory.

