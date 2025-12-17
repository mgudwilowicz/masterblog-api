from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == "POST":
        id = max(post['id'] for post in POSTS) + 1
        data = request.get_json()
        print(data)
        if not validate_post_data(data):
            return jsonify('Title or Content is missing'), 400
        new_post = {'id': id, 'title': data['title'], 'content': data['content']}

        POSTS.append(new_post)
        return jsonify(new_post), 201

    return jsonify(POSTS)


@app.route('/api/posts/<int:id>', methods=['DELETE'])
def delete(id):
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"message": f"Post with id {id} not found"}), 404

    POSTS.remove(post)
    return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200


@app.route('/api/posts/<int:id>', methods=['PUT'])
def update(id):
    post = find_post_by_id(id)
    if post is None:
        return jsonify({"message": f"Post with id {id} not found"}), 404

    data = request.get_json()
    post.update(data)

    return jsonify(post), 200


def validate_post_data(post):
    if post['title'] == '' or post['content'] == '':
        return False
    return True


def find_post_by_id(id):
    for post in POSTS:
        if post['id'] == id:
            return post
    return None


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
