from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file and file.filename.endswith('.xlsx'):
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)
        return redirect(url_for('display_file', filename=file.filename))
    return redirect(url_for('index'))

@app.route('/display/<filename>')
def display_file(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    df = pd.read_excel(file_path, dtype=str)
    data = df.to_html(classes='data', header="true", index=False)
    return render_template('display.html', table=data)

if __name__ == '__main__':
    app.run(debug=True)