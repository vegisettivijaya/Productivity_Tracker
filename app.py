from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task_title = request.form["task"]
        new_task = Task(title=task_title)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("index"))

    tasks = Task.query.order_by(Task.date_created.desc()).all()
    return render_template("index.html", tasks=tasks)
@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = Task.query.get(task_id)
    task.completed = True
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))
@app.route("/stats")
def stats():
    total_tasks = Task.query.count()
    completed_tasks = Task.query.filter_by(completed=True).count()
    return render_template("stats.html", total_tasks=total_tasks, completed_tasks=completed_tasks)
if _name_ == "_main_":
    app.run(debug=True)
