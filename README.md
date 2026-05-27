# League of Legends Stat Tracker

**League of Legends Stat Tracker** is a local analytics application that collects match data through the Riot APIs, stores them in a SQLite database, and provides a Flask web interface for viewing statistics and visualizing performance.


## Features

- **Lightweight**
- **Cross-browser support**
- **Modular pipeline**

## Built With
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)   
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)  
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)  
![HTML](https://img.shields.io/badge/HTML5-%23F24E1E.svg?style=for-the-badge&logo=HTML5&logoColor=white)   
![CSS](https://img.shields.io/badge/css-%23663399.svg?style=for-the-badge&logo=css&logoColor=white)


# Table of Contents
- [Getting Started](#getting-started)
- 



# Getting Started

To get a local copy running, follow these steps.

## Obtain a Riot API Key

1. Create a Riot Account and login to: https://developer.riotgames.com/

2. On the main page, regenerate the API key and store it for later:  
<img width="600" src="https://github.com/ryanjj-chew/Readme_Assets/Regenerate_api_key.jpg">

## Prerequisites
1. Install Python 3+ (Preferably the latest version) from: [Python Download Link](https://www.python.org/downloads/)

2. Clone the repository:  
```bash
git clone https://github.com/ryanjj-chew/LeagueTracker
```

3. Create a Virtual Environment (venv) in the Root of the Cloned Repository in Powershell:  
```bash
python -m venv C:\path\to\new\virtual\environment
```

4. Activate the Virtual Environment:  
```bash
.venv\Scripts\activate
``` 
> Note: On Microsoft Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following PowerShell command:  
`PS C:\> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`  
Please refer to https://docs.python.org/3/library/venv.html for more information.

5. Install the prerequisites:
```bash
pip install -r requirements.txt
```

6. Run the App:  
```bash
python app.py
```

7. Open the Flask server in Google Chrome/Microsoft Edge:  
```bash
http://127.0.0.1:5000
```

