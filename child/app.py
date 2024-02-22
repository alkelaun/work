from flask import Flask, render_template
import os

app = Flask(__name__)
storage_path = '/app/files/'

@app.route('/')
def index():
    files = os.listdir(storage_path)
    return render_template('index.html', files=files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)