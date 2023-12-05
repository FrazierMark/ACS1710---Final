from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
import certifi
from pymongo.server_api import ServerApi
from datetime import timezone, datetime

app = Flask(__name__)

uri = "mongodb+srv://markms89:password123456@cluster0.r5pcvhu.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

db = client.todos
todos = db.todosCollection

#Check if the connection was successful
#Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

except Exception as e:
    print(e)

# Create a new todo or retrieve all todos
@app.route('/', methods=('GET', 'POST'))
def index():
    if request.method=='POST':
        content = request.form['content']
        degree = request.form['priority']
        todos.insert_one({'content': content, 'priority': degree, 'completed': False, 'created': datetime.now(timezone.utc)})
        return redirect(url_for('index'))

    all_todos = todos.find().collation({'locale': 'en'}).sort('content')
    return render_template('index.html', todos=all_todos) # add todos here! 


# Update the status of the todo
@app.post('/<id>/update/')
def update(id):
    filter = { '_id': ObjectId(id) }
    new_values = { '$set': { 'completed': True } }
    todos.update_one(filter, new_values)
    
    return redirect(url_for('index'))

# Delete the todo
@app.post('/<id>/delete/')
def delete(id):
    todos.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
