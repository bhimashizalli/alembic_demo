import os
from datetime import datetime
from flask import Flask, request, jsonify, render_template
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from models import User, Task, Category, Base
from sqlalchemy.exc import IntegrityError

# Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise EnvironmentError("Environment variable 'DATABASE_URL' is not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize Flask app
app = Flask(__name__)

# Setup for Templates and Static Files
app.static_folder = 'static'
app.template_folder = 'templates'

# Initialize database (only necessary during setup)
# Base.metadata.create_all(bind=engine)

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
    except IntegrityError as e:
        session.rollback()
        return jsonify({"error": "User already exists!"}), 400
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
        return jsonify(
            [{"id": user.id, "username": user.username, "email": user.email, "created_at": user.created_at} for user in
             users]
        )
    finally:
        session.close()

@app.route("/task", methods=["POST"])
def create_task():
    session = SessionLocal()
    try:
        title = request.json["title"]
        description = request.json.get("description", "")
        user_id = request.json["user_id"]
        is_complete = request.json.get("is_complete", False)
        due_date = request.json.get("due_date", None)
        category_id = request.json.get("category_id", None)

        task = Task(
            title=title,
            description=description,
            user_id=user_id,
            is_complete=is_complete,
            due_date=due_date,
            category_id=category_id,
        )
        session.add(task)
        session.commit()
        return jsonify({"message": "Task created successfully", "task_id": task.id}), 201
    except IntegrityError:
        session.rollback()
        return jsonify({"error": "User or Category does not exist"}), 400
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/tasks", methods=["GET"])
def get_tasks():
    session = SessionLocal()
    try:
        # Extract query parameters
        user_id = request.args.get("user_id", type=int)
        category_id = request.args.get("category_id", type=int)
        due_date_str = request.args.get("due_date", type=str)

        query = session.query(Task)  # Start base query

        # Apply filters
        if user_id:
            query = query.filter(Task.user_id == user_id)
        if category_id:
            query = query.filter(Task.category_id == category_id)
        if due_date_str:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()  # Convert string to date
            query = query.filter(Task.due_date == due_date)

        tasks = query.all()  # Execute query

        return jsonify([
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.is_complete,
                "due_date": task.due_date,
                "priority": task.priority,
                "user_id": task.user_id,
                "category_id": task.category_id,
            }
            for task in tasks
        ])
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/task/<int:task_id>", methods=["PATCH"])
def complete_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.is_complete = not task.is_complete
            session.commit()
            return jsonify({"message": "Task status updated", "task_id": task.id})
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            session.delete(task)
            session.commit()
            return jsonify({"message": "Task deleted successfully"}), 200
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

@app.route("/update_task/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    session = SessionLocal()
    try:
        task = session.query(Task).filter(Task.id == task_id).first()
        if task:
            task.title = request.json.get("title", task.title)
            task.description = request.json.get("description", task.description)
            task.is_complete = request.json.get("is_complete", task.is_complete)
            task.due_date = request.json.get("due_date", task.due_date)
            task.category_id = request.json.get("category_id", task.category_id)
            session.commit()
            return jsonify({"message": "Task updated successfully", "task_id": task.id})
        else:
            return jsonify({"error": "Task not found"}), 404
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400
    finally:
        session.close()

if __name__ == "__main__":
    app.run(debug=True)