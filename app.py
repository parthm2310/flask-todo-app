from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
import uuid
import hashlib

app = Flask(__name__)

# MongoDB Setup
client = MongoClient("mongodb://localhost:27017/")
db = client["todoDB"]
collection = db["todoItems"]

@app.route('/')
def home():
    todos = collection.find()
    return render_template('index.html', todos=todos)

@app.route('/submittodo', methods=['POST'])
def submit_todo():
    item_name = request.form['itemName']
    item_description = request.form['itemDescription']
    item_id = request.form.get('itemId', '')
    item_uuid = request.form.get('itemUUID', str(uuid.uuid4()))
    item_hash = hashlib.sha256(f"{item_name}{item_description}".encode()).hexdigest()

    todo = {
        'itemId': item_id,
        'itemName': item_name,
        'itemDescription': item_description,
        'itemUUID': item_uuid,
        'itemHash': item_hash
    }
    collection.insert_one(todo)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
