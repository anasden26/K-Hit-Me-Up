from flask import Flask, render_template, request
import pandas as pd
import pickle

filename = "clf.sav"
model = pickle.load(open(filename, 'rb'))

def get_data(data):
    data.drop(["artist", "popularity"],axis=1,inplace=True)
    predicted = model.predict(data)
    popular = sum(predicted==1)
    total = len(predicted)
    return popular, total

def get_data_from_year(year):
    if (year == '2011'):
        raw_data = pd.read_csv('spotify_top_kpop_2011.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2012'):
        raw_data = pd.read_csv('spotify_top_kpop_2012.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2013'):
        raw_data = pd.read_csv('spotify_top_kpop_2013.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2014'):
        raw_data = pd.read_csv('spotify_top_kpop_2014.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2015'):
        raw_data = pd.read_csv('spotify_top_kpop_2015.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2016'):
        raw_data = pd.read_csv('spotify_top_kpop_2016.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2017'):
        raw_data = pd.read_csv('spotify_top_kpop_2017.csv').sort_values(by=['song_popularity'], ascending=False)
    elif (year == '2018'):
        raw_data = pd.read_csv('spotify_top_kpop_2018.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2019'):
        raw_data = pd.read_csv('spotify_top_kpop_2019.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2020'):
        raw_data = pd.read_csv('spotify_top_kpop_2020.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2021'):
        raw_data = pd.read_csv('spotify_top_kpop_2021.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    elif (year == '2022'):
        raw_data = pd.read_csv('spotify_top_kpop_2022.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    length = len(raw_data)
    title = raw_data['title']
    artist = raw_data['artist']
    return length, title, artist

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/popularity", methods=['GET'])
def popularity():
    return render_template(
        "prev_year.html",
        data = [
            {'year': '2011'},
            {'year': '2012'},
            {'year': '2013'},
            {'year': '2014'},
            {'year': '2015'},
            {'year': '2016'},
            {'year': '2017'},
            {'year': '2018'},
            {'year': '2019'},
            {'year': '2020'},
            {'year': '2021'},
            {'year': '2022'},
        ]
    )

@app.route("/popularity-picked", methods=['GET', 'POST'])
def popularity_picked():
    year = request.args['year']
    result = get_data_from_year(year)
    state = {'data': year}
    return render_template(
        "prev_year_picked.html",
        data = [
            {'year': '2011'},
            {'year': '2012'},
            {'year': '2013'},
            {'year': '2014'},
            {'year': '2015'},
            {'year': '2016'},
            {'year': '2017'},
            {'year': '2018'},
            {'year': '2019'},
            {'year': '2020'},
            {'year': '2021'},
            {'year': '2022'},
        ],
        length = result[0],
        index = year,
        title = result[1],
        artist = result[2],
        state = state
    )

@app.route("/artist")
def artist():
    return render_template("artist.html")

@app.route("/artist-result", methods=['POST'])
def artistresult():
    name = request.form['kpopartist']
    name = name.upper()
    data_edited = pd.read_csv('spotify_data_edited_with_artist.csv')
    data_edited['artist'] = data_edited['artist'].str.upper()
    data_edited_2 = data_edited[data_edited['artist']==name]
    if(len(data_edited_2)==0):
        return render_template(
            "result_not_found.html",
            artist = name
        )
    else:
        result = get_data(data_edited_2)
        return render_template(
            "artist-result.html", 
            result_positive = result[0],
            result = result[1],
            name = name
        )

@app.route("/artist2023")
def artist2023():
    data_edited = pd.read_csv('spotify_kpop_2023_edited.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    raw_data = pd.read_csv('spotify_kpop_2023.csv').sort_values(by=['song_popularity'], ascending=False, ignore_index=True)
    data_edited.drop(["artist", "song_popularity", "popularity", "time_signature_1.0"],axis=1,inplace=True)
    predicted = model.predict(data_edited)
    total = len(predicted)
    artist = raw_data['artist']
    title = raw_data['title']
    popularity = raw_data['song_popularity']
    predicted = ["Yes" if value == 1 else "No" for value in predicted]
    return render_template(
        "result.html",
        length = total,
        artist = artist,
        title = title,
        song_popularity = popularity,
        popular = predicted
    )