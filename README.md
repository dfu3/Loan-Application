# Loan-Application
Flask App that takes user's loan application data and returns a resulting offer


## Setup
(after cloning repo, checkout master branch, and ensure you have python installed)

Intall Postgresql, and setup a local DB
create a user and give them access to the DB
export usernmae and password as the following ENV Vars: DB_USERNAME and DB_PASSWORD

This project installs its dependencies using a python virtual env:
(Windows OS)
```
PS> python -m venv venv
PS> .\venv\Scripts\activate
(venv) PS>
```
( if you get an error when activating the env^ try running the following in an admin shell: `set-executionpolicy remotesigned`)

After setting up your VE, install dependenices using:
```
(venv) $ python -m pip install -r requirements.txt
```

Initialize the DB:
```
python init_db.py
```
