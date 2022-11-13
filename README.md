# GyaanOverFlow

* This forum service is built using HTML, CSS, JavaScript, Flask, and MongoDB Atlas for storing the data.
* The live demo link for the app: http://gyaanoverflow.onrender.com/

## Project Structure

The `GOF` directory holds the application logic. 
* `Ask_Anything/__init__.py` handles the all actions regrading questions and their comments.
* `Registration/__init__.py` handles the SignUp, SignIn and SignOut feature.
* `main/__init__.py` handles the all blueprints of this flask application as well as deal with Ajax responses.
* `static` contains images, CSS and JavaScript files.
* `templates` contains all html pages.
* `SearchEngine.py` It handles the content based search feature using Natural Language Processing consepts.
* `__init__.py` configure the Flask application
* `extension.py` connect the flask application with MongoDB Atlas

The main directory holds the following files:
* `app.py` it starts the flask application
* `Prockfile` is for render deployment
* `requirments.txt` contains required python libraries




## How to set-up

Clone the repository.
```
git clone git@github.com:JARVIS1612/gyaanoverflow.git
```

Start a python virtual env:
```
# navigate to the flask-pymongo-example directory
cd gyaanoverflow
# create the virtual environment for MFlix
python3 -m venv mflix-venv
# activate the virtual environment
source mflix_venv/bin/activate
```

Install dependencies
```
python3 -m pip install -r requirments.txt
```



## Start the application

```
python ./run.py
```
Open your browser on http://localhost:5000
