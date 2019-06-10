# kobo_api

This repo will feature sample code/snippets to pull or push data (or form definitions) using the new [KoBoToolbox API ](https://github.com/kobotoolbox/kpi/)

## get_csv.py

[get_csv.py](https://github.com/tinok/kobo_api/blob/master/get_csv.py) is a command line script written in Python that allows users to 
* Create a new export for a given kobo asset (project)
* Allows customizing the export with all available options (can be passed as arguments)
* Get a list of all previous exports
* Get the URL of the most recent export
* Uses basic authentication (username and password), which can be entered into the file or saved as an environment variable 

## Usage instructions
* Requires Python on your computer/virtual machine.
* Download the file or clone the repository
* Edit the [four variables](https://github.com/tinok/kobo_api/blob/master/get_csv.py#L19-L22) specific to your account and project. Note that `koboassetid` refers to the unique string included in the URL of the project, e.g. `https://kobo.humanitarianresponse.info/#/forms/aLLE5AEVsxzwiBCcinzWrF/summary`.

The script has four commands:

* `python get_csv.py create` to generate the default export (xml values, csv format, all versions included, don't show group hierarchy, separate groups/select_multiple options with `/`). 
  * These defaults can be changed [here](https://github.com/tinok/kobo_api/blob/master/get_csv.py#L26-L30), or they can be overriden with flags (e.g. `create -t csv -l 'English (en_US)' -f true`
* `python get_csv.py latest` to get a URL to download the most recent export
* `python get_csv.py list` to see a list of all previously created exports

For help run `python get_csv.py -h`

We'd love an R version of this script.


## Help needed!

We would love contributions of other scripts for other purposes (R, Python, or other languages) that can be used as standalone scripts for other users.

