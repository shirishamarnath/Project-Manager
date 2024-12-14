from flask import Flask, render_template, request, redirect, url_for
from firebase_functions import upload_file, manage_file, view_file

app = Flask(__name__,static_folder="static")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    return upload_file()

@app.route('/manage')
def manage():
    return manage_file()

@app.route('/view/<file_id>')
def view(file_id):
    # Simply return the result of view_file, which already renders the template
    return view_file(file_id)

if __name__ == '__main__':
    app.run(debug=True)
