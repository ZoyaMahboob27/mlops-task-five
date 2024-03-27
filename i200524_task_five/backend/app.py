from flask import Flask, request, jsonify
from pymongo import MongoClient
import random
import string

app = Flask(__name__)

# MongoDB connection
mongo_client = MongoClient('mongodb://mongodb:27017/')
db = mongo_client['my-web-app']
users_collection = db['users']

def generate_nickname(name, email):
    # Generate a random nickname based on the name and email
    nickname_length = 8
    allowed_chars = string.ascii_letters + string.digits
    nickname = ''.join(random.choice(allowed_chars) for _ in range(nickname_length))
    return nickname

@app.route('/submit', methods=['POST'])
def submit_data():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')

    # Store the data in the MongoDB database
    user = {'name': name, 'email': email}
    users_collection.insert_one(user)

    # Generate a random nickname
    nickname = generate_nickname(name, email)

    return jsonify({'nickname': nickname})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)