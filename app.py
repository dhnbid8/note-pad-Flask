from sqlite3 import IntegrityError
from flask import Flask, redirect, render_template, redirect, request
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# app
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.String(100), index=True)
    body = db.Column(db.String(1000), index=True)

    def __repr__(self):
        return '<title {}>'.format(self.title)
        
    def save(self):
        try:
            db.session.add(self)
            db.session.flush()
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ApiException(e.__str__(), 201)
        except Exception as e : 
            db.session.rollback()
            raise ApiException(e.__str__(), 201)

@app.route('/')
def index():
    notes = Note.query.all()
    return render_template('index.html', notes=notes)

@app.route('/block/<int:id>')
def block(id):
    note = Note.query.get(id)
    if(note):
        return render_template('datile.html', note=note)
    else:
        return render_template('index.html')

@app.route('/add-note', methods=["POST", "GET"])
def addNote():
    if request.method == "POST":
        title = request.form.get("title")
        body = request.form.get("editor1")
        note = Note(title= title, body=body)
        db.session.add(note)
        db.session.commit()
        return redirect ("/")
    else:
        return render_template("addnote.html")

@app.route('/edit/<int:id>', methods=["POST", "GET"])
def updateNote(id):
    note = Note.query.get(id)
    if note :
        if request.method == "POST":
            note.title = request.form.get("title")
            note.body = request.form.get("editor1")
            note.save()
            return redirect ("/")
    
        return render_template("edit.html", note= note)
    else:
        return redirect("/")


@app.route('/delete/<int:id>')
def delete_note(id):
    note = Note.query.get(id)
    if(note):
        db.session.delete(note)
        db.session.commit()
        return redirect("/")
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()