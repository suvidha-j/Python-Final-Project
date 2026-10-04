from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []
next_id = 1


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Python Task Management API",
        "status": "running"
    })


@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


@app.route("/tasks", methods=["POST"])
def create_task():
    global next_id

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    title = data.get("title", "").strip()

    if not title:
        return jsonify({
            "error": "Task title is required"
        }), 400

    task = {
        "id": next_id,
        "title": title,
        "completed": False
    }

    tasks.append(task)
    next_id += 1

    return jsonify(task), 201


@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = next(
        (item for item in tasks if item["id"] == task_id),
        None
    )

    if task is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400

    if "title" in data:
        title = str(data["title"]).strip()

        if not title:
            return jsonify({
                "error": "Task title cannot be empty"
            }), 400

        task["title"] = title

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({
                "error": "Completed must be true or false"
            }), 400

        task["completed"] = data["completed"]

    return jsonify(task), 200


@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = next(
        (item for item in tasks if item["id"] == task_id),
        None
    )

    if task is None:
        return jsonify({
            "error": "Task not found"
        }), 404

    tasks.remove(task)

    return jsonify({
        "message": "Task deleted successfully"
    }), 200


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({
        "error": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "error": "Internal server error"
    }), 500


if __name__ == "__main__":
    app.run(debug=True)