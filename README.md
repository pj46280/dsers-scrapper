# Automate scrapping products from https://www.dsers.com

## Introduction

Must have an account on dsers.com for account credential

## Working

* Create `config.ini` in the project directory and add account credentials as shown in `demo_config.ini`

* Create virtualenvironment in the project directory -

```
python -m venv venv
```

* Activate virtual environment and install dependencies -

```
source venv/bin/activate
pip install -r requirements
```

* Run the main script

```
python main.py
```

## Output

`output.xlsx` will be present in the project directory after script executes successfully.

## Data

In the `main.py` on line no. 170, change the `details` list accordingly to extract data of choice

Product url must be provided in the `details` list, rest of the data is for user's ease of use and formatting.
