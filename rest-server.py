#!flask/bin/python
import six, os, time
from flask import Flask, jsonify, abort, request, redirect, make_response, url_for
from werkzeug.utils import secure_filename

from clamscan import scan

UPLOAD_FOLDER = '/usr/src/app/download'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__, static_url_path="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


tasks = []

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


@app.route('/files', methods=['POST'])
def upload_file():
    f = request.files['file']
    if f.filename == '':
        abort(400)
    if not f or not allowed_file(f.filename):
        abort(400)
    ts = str(int(time.time()))
    ori_filename = secure_filename(f.filename)
    filename = ts + "_" + ori_filename
    f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    size = os.stat(app.config['UPLOAD_FOLDER'] + '/' + filename).st_size
    
    cr, message = scan(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    
    if len(tasks) == 0:
        task_id = 1
    else:
        task_id = tasks[-1]['id'] + 1
    task = {
        'id': task_id,
        'file': ori_filename,
        'path_name': filename,
        'size': size,
        'scan_result': message,
        'return_code': cr,
        'done': True
    }
    tasks.append(task)
    
    return jsonify(task), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

