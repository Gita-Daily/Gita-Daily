from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/web', methods=['POST'])
def respond():
    try:
        print(request.json)
        return jsonify(status="received"), 200
    except Exception as e:
        print('error: ' + str(e))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)