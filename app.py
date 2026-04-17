from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ToDo {self.id}>'

@app.route("/")
def index():
    tasks = Todo.query.all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task_content = request.form['content']
    new_task = Todo(content=task_content)
    db.session.add(new_task)
    db.session.commit()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect("/")

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == "POST":
        task.content = request.form['content']
        db.session.commit()
        return redirect("/")
    return render_template("update.html", task=task)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) 