from flask import Flask
from flask import request
from flask import abort

from werkzeug import secure_filename
from pathlib import Path
import os
import sqlite3

UPLOAD_FOLDER = os.path.join(str(Path(__file__).resolve().parent.parent), "uploads")
ALLOWED_EXTENSIONS = set(['db'])

from OpenSSL import SSL
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('ssl_cert/example.key')
context.use_certificate_file('ssl_cert/example.crt')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def is_sqlite(file):
    '''
    Make sure the uploaded file is a legit SQLite3 file
    '''
    try:
        conn = sqlite3.connect(file)
    except:
        return False
    return True

@app.route('/')
def root():
  return "It's working!"

@app.route('/upload', methods = ['POST'])
def upload_file():
  if request.method == 'POST':
    f = request.files['file']
    file_name = secure_filename(f.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
    try:
        f.save(file_path)
        if is_sqlite(file_path):
            return 'file uploaded successfully'
        else:
            os.remove(file_path)
            abort(400)
    except:
        abort(500)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=443, ssl_context=context)
