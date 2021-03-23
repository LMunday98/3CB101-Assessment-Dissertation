import time
from flask import Flask, Response, redirect, request, url_for, render_template, jsonify, stream_with_context
from app import app

@app.route('/')
def root():
    return render_template('public/index.html')
