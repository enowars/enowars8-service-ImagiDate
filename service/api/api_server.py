from flask import Flask, request, jsonify
import yaml
import os
import hashlib

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def generate_user_directory(username):
    hashed_username = hashlib.md5(username.encode()).hexdigest()
    user_directory = os.path.join(app.config['UPLOAD_FOLDER'], hashed_username)
    if not os.path.exists(user_directory):
        os.makedirs(user_directory)
    return user_directory


@app.route('/test_my_luck', methods=['POST'])
def parse_yaml():
    try:
        username = request.form.get('username')
        if not username:
            return jsonify({'success': False, 'error': 'Username not provided.'}), 400
        
        user_directory = generate_user_directory(username)

        yaml_data = request.files['file'].read().decode('utf-8')
        parsed_data = yaml.load(yaml_data)

        # Validate YAML structure
        if not isinstance(parsed_data, dict):
            return jsonify({'success': False, 'error': 'Invalid YAML structure.'}), 400

        # Extract user data
        user_info = {
            'username': parsed_data.get('username'),
            'age': parsed_data.get('age'),
            'gender': parsed_data.get('gender'),
            'requested_username': parsed_data.get('requested_username'),
            'punchline': parsed_data.get('punchline')
        }
        
        # Store the YAML file
        filename = request.files['file'].filename
        file_path = os.path.join(user_directory, filename)
        with open(file_path, 'w') as file:
            file.write(yaml_data)
        
        return jsonify({'success': True, 'user_info': user_info}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)