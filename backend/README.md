# DnDEZ  
DnDEZ web app for managing sessions with other players

## Dependencies ##
1. python3.8 or greater 
2. everything in requirements.txt
3. Sqlite3
4. foreman (install how-to: https://github.com/ddollar/foreman)
5. GNU make

## How to run ##

# (note: this project is inteded to be developed in a python venv)
1. Install venv for your python version (pip3 install virtualenv)
2. Create a virtual environment (python3.x -m venv put_name_here)
3. navigate into the new folder (cd folderName)
4. activate the venv (source bin/activate)
5. clone this repo 
6. cd into the repo and install the requirements (pip3 install -r requirements.txt)
7. navigate to the /database/schemas folder 
8. make
9. navigate to the /backend folder 
10. Change the value of "FLASK_RUN_HOST" in the .env file to your preffered address (by default it should be localhost)
11. run "foreman start -p 5000" (this runs the webapp on port 5000, you can change the value after "-p" to change the port number)

You should now be able to access the app on http://localhost:5000 (or whatever values you used for .env and -p)