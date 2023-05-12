from flask import Flask, request, jsonify
from makeGraph import generate_plot
import io

app = Flask(__name__)

@app.route('/generate_plot', methods=['POST'])
def generate_plot_endpoint():
    x_data = request.json['x_data']
    y_data = request.json['y_data']

    fig = generate_plot(x_data, y_data)

    img_data = io.BytesIO()
    fig.savefig(img_data, format='png')
    img_data.seek(0)
    return img_data.read()


if __name__ == '__main__':
    app.run(debug=True)
