from flask import Flask, render_template, request, redirect, flash

from bson.objectid import ObjectId
from flask.helpers import flash

import pymongo

import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


app= Flask('contact-manager')

app.config['SECRET_KEY'] = 'contact'

client = pymongo.MongoClient('mongodb+srv://richardlin:richardlin@cluster0.3wovn.mongodb.net/myDatabase?retryWrites=true&w=majority')

db = client.contactmanager

@app.route('/', methods= ['GET','POST'])
def index():
    if request.method == 'GET':
        contacts =db.contacts.find()
        return render_template('index.html',contacts = contacts )
    if request.method == 'POST':
        print(request.form)
        document = {}
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        document = {'name':name, 'number':number,'email':email}
        if len(name) < 3:
            flash('Name cannot have less than 3 characters.')
            return redirect('/')
        if not re.match(regex, email):
            flash('Invalid Email')
            return redirect('/')
        db.contacts.insert_one(document)
        flash('adding a contact successfully')
        return redirect('/')

@app.route('/delete/<contact_id>')
def delete(contact_id):
    db.contacts.delete_one({'_id':ObjectId(contact_id)})
    flash('deleting a contact successfully')
    return redirect('/')


@app.route('/update/<contact_id>', methods = ['GET',"POST"])
def update(contact_id):
    contact = db.contacts.find_one({'_id':ObjectId(contact_id)})
    print(contact_id)
    if request.method == 'GET':
        return render_template('update.html', contact = contact)
    if request.method == 'POST':
        document = {}
        name = request.form['name']
        number = request.form['number']
        email = request.form['email']
        document = {'name':name, 'number':number,'email':email}
        print(contact)
        if len(name) < 3:
            flash('Name cannot have less than 3 characters.')
            return redirect('/update/'+contact_id)
        if not re.match(regex, email):
            flash('Invalid Email')
            return redirect('/update/'+contact_id)
        db.contacts.update_one({'_id':ObjectId(contact_id)}, {'$set': document})
        flash('Updating a contact successfully')
        return redirect('/')

if __name__=='__main__':
    app.run(debug=True)