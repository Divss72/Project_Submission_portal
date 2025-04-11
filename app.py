from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
import csv
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure CSV file exists
csv_file = 'submissions.csv'
if not os.path.isfile(csv_file):
    with open(csv_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Name', 'UID', 'Filename', 'Timestamp'])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        uid = request.form['uid']
        file = request.files['projectFile']
        
        if file and name and uid:
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            with open(csv_file, mode='a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, uid, filename, timestamp])
            
            return f"<h2>Submission successful!</h2><p>{name} ({uid}) uploaded <b>{filename}</b> at {timestamp}.</p><a href='/'>Submit another</a>"

        return "Missing data or file!", 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
csv_file = 'submissions.csv'

try:
    if not os.path.isfile(csv_file):
        with open(csv_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'UID', 'Filename', 'Timestamp'])
except PermissionError:
    print(f"❌ Cannot write to {csv_file}. Please check permissions or close any apps using it.")
