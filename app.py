from flask import Flask, request, jsonify
import docker
import random
import string
import os

app = Flask(__name__)
client = docker.from_env()

# In-memory storage for simplicity. Replace with a database in production.
services = {}

@app.route('/services', methods=['POST'])
def register_service():
    data = request.json
    github_url = data.get('github_url')
    
    if not github_url:
        return jsonify({"error": "GitHub URL is required"}), 400
    
    service_id = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    port = random.randint(10000, 11000)
    
    # Create and start the Docker container
    container = client.containers.run(
        "node:14",
        command=f"""
        bash -c '
        git clone {github_url} /app && 
        cd /app && 
        npm install -g express-generator@4 &&
        express /tmp/foo && 
        cd /tmp/foo && 
        npm install && 
        npm start
        '
        """,
        detach=True,
        ports={'3000/tcp': port},
        environment=["PORT=3000"]
    )
    
    services[service_id] = {
        'github_url': github_url,
        'container_id': container.id,
        'port': port
    }
    
    return jsonify({
        "service_id": service_id,
        "url": f"http://localhost:{port}"
    }), 201

@app.route('/services/<service_id>', methods=['GET'])
def get_service(service_id):
    service = services.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    return jsonify({
        "service_id": service_id,
        "url": f"http://localhost:{service['port']}"
    })

@app.route('/services', methods=['GET'])
def list_services():
    return jsonify([
        {
            "service_id": service_id,
            "url": f"http://localhost:{service['port']}"
        } for service_id, service in services.items()
    ])

@app.route('/services/<service_id>', methods=['DELETE'])
def delete_service(service_id):
    service = services.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404
    
    # Stop and remove the Docker container
    container = client.containers.get(service['container_id'])
    container.stop()
    container.remove()
    
    del services[service_id]
    
    return '', 204

if __name__ == '__main__':
    app.run(debug=True)