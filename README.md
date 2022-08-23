# cx2csv - Crowdin xliff 2 csv

It outputs an XLIFF file exported from Crowdin to a CSV or an XLIFF file for applying and importing an edited CSV to an XLIFF.

## Prerequisites

* python 3.10

We confirmed that it works with python installed on Windows and Ubuntu in WSL 2.

```
pip install lxml
```

## Installing

git clone this project.

```
git clone git@github.com:freedomcat/cx2csv.git
pip install lxml
```

## Usage

### First: Export XLIFF to CSV

```
python3 cx2csv.py PATH/TO/YOURS/EXPORT.xliff
```
output: PATH/TO/YOURS/EXPORT.csv

- You can edit the "target" column of PATH/TO/YOURS/EXPORT.csv.

### Generate IMPORT XLIFF from Export XLIFF and Edited CSV

If you edit the CSV created above directly, Specify as follows:
```
python3 cx2csv.py PATH/TO/YOURS/EXPORT.xliff -r
```

Or if you want to replace a CSV file with a different name, use:
```
python3 cx2csv.py PATH/TO/YOURS/EXPORT.xliff -r PATH/TO/YOURS/EDITED.csv
```

output: PATH/TO/YOURS/EXPORT-import.xliff

- You can upload EXPORT-import.xliff to crowdin.

## Authors

shino (@freedomcat)

## LICENSE

freedomcat/cx2csv is licensed under the [MIT License](https://opensource.org/licenses/MIT)

