import os
from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)
db = client.taskdb
collection = db.tasks

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form.get('task')
        if task_content:
            collection.insert_one({"task": task_content})
        return redirect(url_for('index'))
    
    all_tasks = list(collection.find())
    return render_template('index.html', tasks=all_tasks)

# --- DELETE ROUTE ---
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))

# --- EDIT (UPDATE) ROUTE ---
@app.route('/edit/<id>', methods=['POST'])
def edit(id):
    new_content = request.form.get('new_task')
    if new_content:
        collection.update_one({"_id": ObjectId(id)}, {"$set": {"task": new_content}})
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)