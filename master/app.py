from flask import Flask, render_template, request, redirect, url_for
import docker
import random
import socket
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

client = docker.from_env()

@app.route('/')
def index():
    containers = client.containers.list()
    return render_template('index.html', containers=containers)


@app.route('/create_container', methods=['POST'])
def create_container():
    container_name = request.form.get('container_name')
    
    # Generate a random port number between 10000 and 11000
    random_port = random.randint(10000, 12000)
    # Create the container with a unique name and expose the randomly selected port
    container = client.containers.run('child', detach=True, name=container_name, ports={5000: random_port})
    
    return redirect(url_for('index'))

@app.route('/open_child_container/<container_name>')
def open_child_container(container_name):
    # Check if the container is already running
    container = client.containers.get(container_name)
    if container.status != 'running':
        # Start the container if it's not running
        container.start()
    return redirect(url_for('index'))

# TODO: This doesn't work
@app.route('/set_network_settings', methods=['POST'])
def set_network_settings():
    container_name = request.form.get('container_name')
    latency = request.form.get('latency')
    bandwidth = request.form.get('bandwidth')
    print(latency, container_name, bandwidth)
    # Find the container by name
    container = client.containers.get(container_name)
    # Set latency between containers
    container.exec_run(f'tc qdisc add dev eth0 root netem delay {latency}ms')
    # Set bandwidth between containers
    container.exec_run(f'tc qdisc add dev eth0 root tbf rate {bandwidth}mbit burst 32kbit latency 400ms')    
    return redirect(url_for('index'))

@app.route('/destroy_container/<container_id>')
def destroy_container(container_id):
    container = client.containers.get(container_id)
    container.stop()
    container.remove(force=True)
    return redirect(url_for('index'))

@app.route('/echo', methods=['POST'])
def echo():
    data = request.data
    print(data)
    return data

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)