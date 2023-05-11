from flask import Flask
from flask import render_template, jsonify 
from waitress import serve

app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Testing Home Page (Render the test.HTML)
@app.route('/', methods=['GET', 'POST'])
def homepage_test():
    return "hello world"
    #return render_template('index.html')

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = int('5000'), debug = True)
    #serve(app, host="0.0.0.0", port=8080)