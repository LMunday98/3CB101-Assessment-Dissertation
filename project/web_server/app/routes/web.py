import time
from flask import Flask, Response, redirect, request, url_for, render_template, jsonify, stream_with_context
from app import app

@app.route('/')
def root():
    return render_template('public/debug.html')

@app.route('/public/cox')
def cox():
    return render_template('public/cox.html')

@app.route('/public/debug')
def charts():
    return render_template('public/debug.html')
