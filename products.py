from flask import render_template, request, redirect
from connection_file import db, app
from classes_file import Products

@app.route('/products')
def products():
    return "He-he"