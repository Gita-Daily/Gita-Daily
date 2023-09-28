from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/web', methods=['POST'])
def respond():
    print(request.json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)