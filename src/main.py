from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import requests
import json
import time
from core.database import CreateDatabaseInterface
from core.server import AuthenticationManager
import ssl

import patient

db = CreateDatabaseInterface('mongodb', {'host': 'mongo', 'port': 27017, 'database_name': 'test'})
db.add_user('ryen', 'T5TCoAXS3Ng0Fr3')
db.add_user('vivek', 'jr5dXC3mS799sGq')

patient_names = ["John Doe", "Jane Doe", "Jack Horner", "Jill Horner", "Jack Sprat", "Jill Sprat", "John Smith"]
# for name in patient_names:
#     if not db.get_patient(name):
#         print(f"Adding patient {name} to database")
#         db.add_patient("John Doe", patient.get_patient_html_by_name(name))
#     else:
#         print(f"Patient {name} already exists in database")

auth = AuthenticationManager(database=db)

app = Flask(__name__)
# secret key
app.secret_key = 'asdfasdf'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        if auth.login_user(username, password):
            return redirect(url_for('home'))
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    else:
        return render_template('login.html', error="Invalid username or password")

@app.route('/logout', methods=['GET'])
def logout():
    auth.logout_user(session['username'], session['session_id'])
    session['authenticated'] = False
    session['username'] = None
    session['session_id'] = None
    return redirect(url_for('login'))

@app.route('/', methods=['GET'])
@auth.login_session_required
def home():
    return render_template('home.html', username=session.get('username', None))

@app.route('/patients', methods=['GET'])
@auth.login_session_required
def patients():
    return render_template('patients.html', username=session.get('username', None))

@app.route('/patient/<patientid>', methods=['GET'])
@auth.login_session_required
def patient(patientid):
    # Assuming patient_details is an HTML-formatted string
    #patient_details = get_patient_details_from_db(patientid)
    #patient_details = '<h1>Patient Details</h1><p>Patient ID: {}</p>'.format(patientid)
    patient_details = db.get_patient(patientid)
    return render_template('patient.html', patient_details=patient_details)


@app.route('/get_active_nodes', methods=['GET'])
@auth.login_session_required
def get_active_nodes():
    result = requests.get('http://node_server:5000/list_nodes')
    return jsonify(result.json())

@app.route('/make_node', methods=['POST'])
@auth.login_session_required
def make_node():
    node_name = request.json.get('node_name')
    node_ip = '127.0.0.1'
    node_port = int(request.json.get('node_port')) + 9000
    
    if not node_name or not node_ip or not node_port:
        return jsonify({"error": "Insufficient node info!"}), 400
    data = {
        'node_name': node_name,
        'node_ip': node_ip,
        'node_port': node_port
    }
    result = requests.post('http://node_server:5000/make_node', json=data)
    return jsonify(result.json()), result.status_code

@app.route('/delete_node', methods=['POST'])
@auth.login_session_required
def delete_node():
    node_name = request.json.get('node_name')
    if not node_name:
        return jsonify({"error": "Node name is required!"}), 400
    data = {
        'node_name': node_name,
    }

    result = requests.post('http://node_server:5000/delete_node', json=data)
    return jsonify(result.json()), result.status_code

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2) #Change to v1_3 when available
    context.load_cert_chain(certfile='./env/fullchain.pem', 
                            keyfile='./env/privkey.pem')
    #context.verify_mode = ssl.CERT_OPTIONAL

    app.run(ssl_context=context, host='0.0.0.0', debug=False, port=3000)
