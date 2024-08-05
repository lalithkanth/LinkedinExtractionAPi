from flask import Flask, request, jsonify
from linkedin_api import Linkedin
import json
import os

app = Flask(__name__)

# Function to authenticate and handle challenges
def authenticate_linkedin():
    try:
        api = Linkedin('LinkedInDemo@mailinator.com', 'Linkedin@123')
        # Save session cookies to a file to avoid future challenges
        with open('linkedin_cookies.json', 'w') as file:
            json.dump(api.client.session.cookies.get_dict(), file)
        return api
    except linkedin_api.client.ChallengeException as e:
        print("Challenge detected: ", e)
        # Handle the challenge (e.g., prompt user to manually resolve)
        raise e

# Initialize the API with cookies if available
def init_api():
    if os.path.exists('linkedin_cookies.json'):
        if os.path.getsize('linkedin_cookies.json') > 0:
            try:
                with open('linkedin_cookies.json', 'r') as file:
                    cookies = json.load(file)
                api = Linkedin('', '')
                api.client.session.cookies.update(cookies)
                return api
            except json.JSONDecodeError as e:
                print("Error reading cookies: ", e)
                print("Re-authenticating due to invalid cookies file.")
                return authenticate_linkedin()
        else:
            print("Cookies file is empty, re-authenticating.")
            return authenticate_linkedin()
    else:
        print("Cookies file does not exist, authenticating.")
        return authenticate_linkedin()

api = init_api()

@app.route('/get_profile', methods=['POST'])
def get_profile():
    try:
        data = request.get_json()
        profile = data['profile']
        result = api.get_profile(profile)
        return jsonify(result), 200
    except linkedin_api.client.ChallengeException as e:
        return jsonify({'error': 'Challenge detected. Please log in to LinkedIn and complete the challenge.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if name == 'main':
    app.run(debug=True)
