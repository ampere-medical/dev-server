from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import requests
import json
import time
from core.database import CreateDatabaseInterface
from core.server import AuthenticationManager
import ssl

import patient

db = CreateDatabaseInterface('mongodb', {'host': 'localhost', 'port': 27017, 'database_name': 'test'})
db.add_user('ryen', 'T5TCoAXS3Ng0Fr3')
db.add_user('vivek', 'jr5dXC3mS799sGq')

patient_names = ["John Doe", "Jane Doe", "Jack Horner", "Jill Horner", "Jack Sprat", "Jill Sprat", "John Smith"]
for name in patient_names:
    if not db.get_patient(name):
        print(f"Adding patient {name} to database")
        info = patient.get_patient_html_by_name(name)
        db.add_patient(name, info)
    else:
        print(f"Patient {name} already exists in database")
