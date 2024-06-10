from flask import Flask, request, jsonify
from linkedin_api import Linkedin

app = Flask(__name__)

api = Linkedin('lalithdebrizz123@gmail.com', 'smvecaids@123')

@app.route('/get_profile', methods=['POST'])
def get_profile():
    try:
        data = request.get_json()
        profile = data['profile']
        result = api.get_profile(profile)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
