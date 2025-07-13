import os
from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Task, Category, Base

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL')
if not DATABASE_URL:
    raise EnvironmentError("Environment variable 'DATABASE_URL' is not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Flask app
app = Flask(__name__)
app.static_folder = 'static'
app.template_folder = 'templates'

# Create database tables
Base.metadata.create_all(bind=engine)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/user", methods=["POST"])
def create_user():
    session = SessionLocal()
    try:
        username = request.json["username"]
        email = request.json["email"]
        user = User(username=username, email=email)
        session.add(user)
        session.commit()
        return jsonify({"message": "User created successfully", "user_id": user.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/users", methods=["GET"])
def get_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])
    finally:
        session.close()

@app.route("/task", methods=["POST"])
def create_task():
    session = SessionLocal()
    try:
        title = request.json["title"]
        description = request.json.get("description", "")
        user_id = request.json["user_id"]
        due_date = request.json.get("due_date")
        category_id = request.json.get("category_id")
        is_complete = request.json.get("is_complete", False)
        task = Task(title=title, description=description, user_id=user_id, due_date=due_date, category_id=category_id, is_complete=is_complete)
        session.add(task)
        session.commit()
        return jsonify({"message": "Task created successfully", "task_id": task.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    session = SessionLocal()
    try:
        tasks = session.query(Task).all()
        return jsonify([
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                "due_date": task.due_date,
                "user_id": task.user_id,
                "category_id": task.category_id
            }
            for task in tasks
        ])
    finally:
        session.close()

@app.route("/task/<int:task_id>", methods=["PATCH"])
def complete_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.is_complete = True
            session.commit()
            return jsonify({"message": "Task marked as complete", "task_id": task.id})
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/categories", methods=["POST"])
def create_category():
    session = SessionLocal()
    try:
        name = request.json["name"]
        category = Category(name=name)
        session.add(category)
        session.commit()
        return jsonify({"message": "Category created successfully", "category_id": category.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/categories", methods=["GET"])
def get_categories():
    session = SessionLocal()
    try:
        categories = session.query(Category).all()
        return jsonify([{"id": category.id, "name": category.name} for category in categories])
    finally:
        session.close()

# Run the app
if __name__ == "__main__":
    app.run(debug=True)