# kobo_api

This repo will feature sample code/snippets to pull or push data (or form definitions) using the new [KoBoToolbox API ](https://github.com/kobotoolbox/kpi/)

## get_csv.py

[get_csv.py](https://github.com/tinok/kobo_api/blob/master/get_csv.py) is a command line script written in Python that allows users to 
* Create a new export for a given kobo asset (project)
* Allows customizing the export with all available options (can be passed as arguments)
* Get a list of all previous exports
* Get the URL of the most recent export
* Uses basic authentication (username and password), which can be entered into the file or saved as an environment variable 

For help run `python get_csv.py -h'

We'd love an R version of this script.


## Help needed!

We would love contributions of other scripts for other purposes (R, Python, or other languages) that can be used as standalone scripts for other users.

