from flask import Flask, render_template, request
import sqlite3, database, json
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, ValidationError
from database import Database
from session_flask import Session
from dataframe import Data_Flask
from background_images import random_bg
from graph import Graph
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "BxGWP%wez3EG&0kK£"

def load_champions():
    with open("data/champions.json", "r") as file:
        data = json.load(file)
    
    champions = [{"id": champ_id, "name": champ_data["name"]} for champ_id, champ_data in data["data"].items()]

    return champions

def validate_champion(form, field):
    champions = load_champions()
    champion_lookup = {champ["name"].strip().lower(): champ["id"] for champ in champions}
    champion_input = field.data.strip().lower()

    if champion_input not in champion_lookup:
        raise ValidationError("Invalid Champion")

    form.champion_id = champion_lookup[champion_input]
    
    return

class SettingsForm(FlaskForm):
    riot_id = StringField("Riot ID:", validators=[DataRequired()])
    tag = StringField("Tag:", validators=[DataRequired()])
    region = SelectField("Region:", choices=[( 'Americas', 'Americas'), ('Europe', 'Europe'), ('Asia', 'Asia')])
    api_key = PasswordField("Api Key:")
    queue = SelectField("Queue:", choices=[("Ranked", "Ranked"), ("Normal", "Normal"), ("Aram", "Aram")])
    submit = SubmitField("Save Settings")

class PuuidForm(FlaskForm):
    submit = SubmitField("Get Puuid")

class ChampionForm(FlaskForm):
    champion_name = StringField("Champion:", validators=[DataRequired(), validate_champion])
    champion_submit = SubmitField("Search")

class UpdateForm(FlaskForm):
    update_submit = SubmitField("Update matches")

@app.route("/", methods=["GET", "POST"])
def Settings():
    form_settings = SettingsForm()
    status = ""
    bg = random_bg()

    try:
        with open("data/settings.json", "r") as file:
            data = json.load(file)
    except:
        with open("data/settings.json", "w") as file:
            data = {"riot_id": "", "tag": "", "region": "", "queue": "", "api_key": "", "puuid": ""}
            json.dump(data, file, indent=4)


    if request.method == "GET":
        form_settings.riot_id.data = data["riot_id"]
        form_settings.tag.data = data["tag"]
        form_settings.region.data = data["region"]
        form_settings.queue.data = data["queue"]

    if form_settings.submit.data and form_settings.validate_on_submit():
        data["riot_id"] = form_settings.riot_id.data
        data["tag"] = form_settings.tag.data
        data["region"] = form_settings.region.data
        data["queue"] = form_settings.queue.data

        new_api_key = form_settings.api_key.data
        if new_api_key:
            data["api_key"] = new_api_key

        with open("data/settings.json", "w") as file:
            json.dump(data, file)

        try:
            session = Session(name=data["riot_id"], tag=data["tag"], region=data["region"], queue=data["queue"], api_key=data["api_key"])
            data["puuid"] = session.get_puuid()
            with open("data/settings.json", "w") as file:
                json.dump(data, file, indent=4)

        except Exception as e:
            print(e)
            data["puuid"] = ""
            status = "Cannot find player."

    
    return render_template("index.html", bg=bg, data=data, form_settings=form_settings, status=status)

@app.route("/history", methods=["GET", "POST"])
def History():
    form = ChampionForm()
    form_update = UpdateForm()
    champions = load_champions()
    query = ""
    status = ""
    
    bg = random_bg()

    if form_update.update_submit.data and form_update.validate_on_submit():
        with open("data/settings.json", "r") as file:
            data = json.load(file)
        session = Session(name=data["riot_id"], tag=data["tag"], region=data["region"],api_key=data["api_key"], queue="Ranked")
        match_history = session.fetch_match()
        status = session.update_timeline()

        db = Database()
        db.update_table()
        db.update_self_player_timeline()
        db.close()

    if form.champion_submit.data and form.validate_on_submit():
        champion_id = form.champion_id
        db = Database()

        with open("data/settings.json", "r") as file:
            settings = json.load(file)
        
        riot_id = settings["riot_id"]
        tag = settings["tag"]
        region = settings["region"]
        api_key = settings["api_key"]
        queue = settings["queue"]
        puuid = settings.get("puuid", "")
        
        rows = db.get_champion_matches(puuid=puuid, champion=champion_id)        
        db.close()

        data = Data_Flask()
        query = data.return_stats(rows)
    
    else:
        db = Database()
        
        with open("data/settings.json", "r") as file:
            settings = json.load(file)
        
        riot_id = settings["riot_id"]
        tag = settings["tag"]
        region = settings["region"]
        api_key = settings["api_key"]
        queue = settings["queue"]
        puuid = settings.get("puuid", "")

        rows = db.get_matches(puuid=puuid)
        db.close()

        data = Data_Flask()
        query = data.return_stats(rows)

    return render_template("history.html", bg=bg, champions=champions, form=form, form_update=form_update, query=query, status=status)

@app.route("/match/<match_id>")
def match_details(match_id):
    bg = random_bg()

    folder = "static/graphs"
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)

        if file.endswith(".png"):
            os.remove(file_path)

    db = Database()
    match_timeline_rows = db.get_match_timeline(match_id)
    db.close()
    
    data = Data_Flask()
    df_wide, df_long = data.return_timeline_stats(match_timeline_rows)

    graph = Graph()
    timeline_graph_path = graph.timeline_graph(df_long, match_id)
    diff_graph_path = graph.timeline_diff_graph(df_wide, match_id)
    cs_graph_path = graph.timeline_cs_graph(df_wide, match_id)

    return render_template("match_id.html", bg=bg, match_id=match_id, timeline_graph_path=timeline_graph_path, diff_graph_path=diff_graph_path, cs_graph_path=cs_graph_path)

if __name__ == "__main__":
    app.run(debug=True)