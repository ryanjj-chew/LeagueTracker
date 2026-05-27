# League of Legends Stat Tracker

<style> body {text-align: justify}
</style>
**League of Legends Stat Tracker** is a local analytics application that collects match data through the Riot APIs, stores them in a SQLite database, and provides a Flask web interface for viewing statistics and visualizing performance.


## Features

- **Lightweight**
- **Cross-browser support**
- **Modular pipeline**

## Built With
![Python](https://img.shields.io/badge/Python-3.13-blue?logo=Python)  
![Flask](https://img.shields.io/badge/Flask-3.1.3-green?logo=Flask)  
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?logo=SQLite)  
![HTML](https://img.shields.io/badge/HTML-5-yellow?logo=HTML5)


## Getting Started

To get a local copy running, follow these steps.

### Prerequisites
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

5. Run the App:  
```bash
python app.py
```
Open the Flask server in your Google Chrome/Microsoft Edge:  
```text
http://127.0.0.1:5000
```