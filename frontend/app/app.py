from flask import Flask
from flask import render_template, jsonify 

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

#Home Page
@app.route('/')
def homepage_test():
    return render_template('index.html')

# Sentiment vs. Location
@app.route('/SentiLocation')
def sentilocation():
    return render_template('SentiLocation.html')

# Mastodon vs. Twitter
@app.route('/MastoTwitter')
def mastotwitter():
    return render_template('mastotwitter.html')

#Member Page
@app.route('/Group_Members')
def members():
    return render_template('members.html')

#Public transport locations
@app.route('/TransportLocations')
def transportlocations():
    return render_template('transportlocations.html')

#Correlation of between public transport locations and sentiment
@app.route('/Correlation')
def correlation():
    return render_template('correlation.html')


if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = int('8080'), debug = True)