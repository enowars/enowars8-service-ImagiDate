from flask import Flask, request, jsonify
import yaml
import os
import hashlib
import secrets

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

harsh_responses = [
    "Are you serious? I would never go out with you.",
    "Not a chance. I’m not interested.",
    "You and me? That’s never going to happen.",
    "Sorry, but I have standards.",
    "No, thanks. You're not my type.",
    "I’d rather stay home and do nothing.",
    "I can't think of anything I'd want to do less.",
    "Absolutely not. Please don't ask again.",
    "No way. I'm not into you.",
    "I'd rather be single than go out with you.",
    "Not in this lifetime.",
    "You must be joking. No.",
    "There's no way I’d consider it.",
    "I don't see you that way, at all.",
    "I don’t date people like you.",
    "I’d rather not waste my time.",
    "I don't find you attractive.",
    "We don’t have anything in common.",
    "You’re not relationship material.",
    "I’m not interested in you, at all.",
    "No, and please stop asking.",
    "I’m not interested in dating anyone right now, especially not you.",
    "There are plenty of fish in the sea, but you're not one of them for me.",
    "I have zero interest in dating you.",
    "That’s a hard pass from me.",
    "I’m sorry, but you’re just not my type.",
    "I don't think we'd get along.",
    "I have no interest in pursuing anything with you.",
    "You’re not someone I want to spend time with.",
    "I’m really not attracted to you in any way."
]

def generate_user_directory(username):
    hashed_username = hashlib.md5(username.encode()).hexdigest()
    user_directory = os.path.join(app.config['UPLOAD_FOLDER'], hashed_username)
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    return user_directory


@app.route('/test_my_luck', methods=['POST'])
def parse_yaml():
    try:

        yaml_data = request.files['file'].read().decode('utf-8')
        parsed_data = yaml.load(yaml_data)

        if not isinstance(parsed_data, dict):
            return jsonify({'success': False, 'error': 'Invalid YAML structure.'}), 400

        user_info = {
            'username': parsed_data.get('username'),
            'age': parsed_data.get('age'),
            'gender': parsed_data.get('gender'),
            'requested_username': parsed_data.get('requested_username'),
            'punchline': parsed_data.get('punchline')
        }
        
        user_directory = generate_user_directory(user_info["username"])

        filename = request.files['file'].filename
        file_path = os.path.join(user_directory, filename)
        with open(file_path, 'w') as file:
            file.write(yaml_data)
        
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/see_my_luck', methods=['GET'])
def get_yaml_file():
    try:
        username = request.args.get("username")
        hashed_username = hashlib.md5(username.encode()).hexdigest()
        user_directory = os.path.join(app.config['UPLOAD_FOLDER'], hashed_username)
        user_input = yaml.dump(open(f"{user_directory}/data.yaml", "r").read())
        match_output = secrets.choice(harsh_responses)

        return jsonify({"success": True, "your_input": user_input, "crush_response": match_output})
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)