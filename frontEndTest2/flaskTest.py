from flask import Flask, request, jsonify
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from flask_cors import CORS


app = Flask(__name__)
CORS(app)











@app.route('/generate_plot', methods=['POST'])
def generate_plot():
    data = request.get_json()
    x = data['x']
    y = data['y']

    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_xlabel('X Axis')
    ax.set_ylabel('Y Axis')

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    data_uri = base64.b64encode(buffer.read()).decode('ascii')
    plt.close()

    response = {'image': data_uri}
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
