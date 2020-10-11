# Shopping Cart  
A simple E-commerce website using Flask.

Project designed to be ran in ubuntu 20.04 or greater. 
  
## Dependencies ##
1. Python3.6 or greater
2. Everything in "requirements.txt"
3. Sqlite3 apt package 
```bash
sudo apt-get install sqlite3
```

## How to run ##
This portion is best set up using python venvs

Make sure you have pip3 installed and the python3 venv module installed 

```bash
sudo apt install python3-pip

sudo apt install -y python3-venv
```

Navigate to a directory you want the project in

To create a venv run:

```bash
python3.x -m venv ProjectFolderName
```
Where "x" is the python3 version desired and "ProjectFolderName" is the name of the project folder

To enable your python virtual environment cd into the projectfoldername and use:

```bash
source bin/activate
```

Your shell should now indicate your env setting being the project 

You can now install dependencies with pip by navigating to the same directory and requirements.txt and running:

```bash
pip3 install -r requirements.txt
```

To deactivate the virtual environment issue the command:

```bash
deactivate
```

1. Set up database by running python3 database.py
2. Run python3 main.py
3. Enter localhost:5000 in the browser.
